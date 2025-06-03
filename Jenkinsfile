pipeline {
    agent any
    environment {
        PYTHON = 'python'  // or 'py' if using Python Launcher
        PROJECT_NAME = 'Python-CICD'

        // Artifact storage path (Windows format)
        //ARTIFACT_DIR = "${env.WORKSPACE}\\artifacts"
        ARTIFACT_DIR = "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Build_PythonProject\\artifacts"
    }

    stages {
        stage('Setup Environment') {
            steps {
                checkout scm
                bat """
                    ${PYTHON} -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install wheel twine pytest
                    mkdir "${ARTIFACT_DIR}"
                """
            }
        }

        stage('Build & Version') {
            steps {
                script {
                    // Get Git commit hash
                    def gitCommit = bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim()

                    // Parse current version from setup.py
                    def currentVersion = readFile('setup.py').find(/version=['"]([^'"]*)['"]/) { match, ver -> ver }

                    // Create new version (0.1.0.buildNumber.commitHash)
                    env.RELEASE_VERSION = "${currentVersion}.${env.BUILD_NUMBER}-${gitCommit}"

                    // Update setup.py with new version (Windows-safe)
                    bat """
                        powershell -Command "(Get-Content setup.py) -replace 'version=\\'[^\\']*\\'', 'version=\\'${env.RELEASE_VERSION}\\'' | Set-Content setup.py"
                    """

                    // Build package
                    bat "${PYTHON} setup.py sdist bdist_wheel"
                }
            }
        }

        stage('Test') {
            steps {
                bat "${PYTHON} -m pytest tests/"
            }
        }

        stage('Archive Artifacts') {
            steps {
                script {
                    // Copy artifacts to workspace artifacts folder
                    bat """
                        if not exist "${ARTIFACT_DIR}" mkdir "${ARTIFACT_DIR}"
                        copy "dist\\*" "${ARTIFACT_DIR}\\"
                    """

                    // Archive in Jenkins (accessible via UI)
                    archiveArtifacts artifacts: 'dist/*', fingerprint: true

                    // Create versioned copies for tracking
                    bat """
                        copy "${ARTIFACT_DIR}\\${PROJECT_NAME}-*.whl" "${ARTIFACT_DIR}\\${PROJECT_NAME}-${env.RELEASE_VERSION}.whl"
                        copy "${ARTIFACT_DIR}\\${PROJECT_NAME}-*.tar.gz" "${ARTIFACT_DIR}\\${PROJECT_NAME}-${env.RELEASE_VERSION}.tar.gz"
                    """
                }
            }
        }

        stage('Tag Release') {
            steps {
                script {
                    // Configure Git (adjust credentials as needed)
                    withCredentials([usernamePassword(
                        credentialsId: 'github-credentials',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )]) {
                        bat """
                            git config --global user.email "jenkins@example.com"
                            git config --global user.name "Jenkins"
                            git tag -a v${env.RELEASE_VERSION} -m "Jenkins release ${env.RELEASE_VERSION}"
                            git push https://${GIT_USER}:${GIT_TOKEN}@github.com/kundansingh06/Python-CICD.git v${env.RELEASE_VERSION}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up build artifacts (keep the archived copies)
            bat 'rmdir /s /q dist build || exit 0'
        }
        success {
            // Print artifact location
            bat """
                echo Artifacts stored in:
                echo ${ARTIFACT_DIR}
                dir "${ARTIFACT_DIR}"
            """
        }
        failure {
            bat 'echo Build failed! Check logs for details.'
        }
    }
}