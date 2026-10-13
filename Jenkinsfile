
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m venv .venv-ci'
                        sh '.venv-ci/bin/python -m pip install -r backend/requirements.txt'
                        sh '.venv-ci/bin/python -m unittest discover -s backend -p "test_*.py" -v'
                    } else {
                        bat 'python -m venv .venv-ci'
                        bat '.venv-ci\\Scripts\\python.exe -m pip install -r backend\\requirements.txt'
                        bat '.venv-ci\\Scripts\\python.exe -m unittest discover -s backend -p "test_*.py" -v'
                    }
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm ci'
                            sh 'npm run build'
                        } else {
                            bat 'npm ci'
                            bat 'npm run build'
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Samvaad CI pipeline completed successfully!'
        }

        failure {
            echo 'Samvaad CI pipeline failed. Check the stage logs.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
