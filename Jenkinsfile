pipeline {
    agent any

    environment {
        PYTHON = 'python'  // or 'py' if using Python Launcher
        PROJECT_NAME = 'Python-CICD'
        ARTIFACT_DIR = "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Build_PythonProject_Pipeline\\artifacts"
    }

    stages {
        stage('Setup Environment') {
            steps {
                // Explicit Git checkout instead of 'checkout scm'
                git(
                    url: 'https://github.com/kundansingh06/Python-CICD.git',
                    credentialsId: 'github-credentials',  // Create in Jenkins Credentials
                    branch: 'main'
                )

                bat """
                    ${PYTHON} -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install wheel twine pytest
                    if not exist "${ARTIFACT_DIR}" mkdir "${ARTIFACT_DIR}"
                """
            }
        }

        stage('Build & Version') {
            steps {
                script {
                    def gitCommit = bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    def currentVersion = readFile('setup.py').find(/version=['"]([^'"]*)['"]/) { match, ver -> ver }
                    env.RELEASE_VERSION = "${currentVersion}.${env.BUILD_NUMBER}-${gitCommit}"

                    // Windows-safe version update
                    bat """
                        powershell -Command "(Get-Content setup.py) -replace 'version=\\'[^\\']*\\'', 'version=\\'${env.RELEASE_VERSION}\\'' | Set-Content setup.py"
                        ${PYTHON} setup.py sdist bdist_wheel
                    """
                }
            }
        }

        stage('Test') {
            steps {
                bat """
                    ${PYTHON} -m pytest tests/ --junitxml=test-results.xml
                    ${PYTHON} -m coverage run -m pytest tests/
                    ${PYTHON} -m coverage xml -o coverage.xml
                """
            }
            post {
                always {
                    junit 'test-results.xml'
                    cobertura 'coverage.xml'
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                bat """
                    copy "dist\\*" "${ARTIFACT_DIR}\\"
                    echo Artifacts stored in: ${ARTIFACT_DIR}
                    dir "${ARTIFACT_DIR}"
                """
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }

        stage('Tag Release') {
            when {
                branch 'main'  // Only tag on main branch
            }
            steps {
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

    post {
        always {
            bat 'rd /s /q dist build || exit 0'  // Cleanup
        }
    }
}