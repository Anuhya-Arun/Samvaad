
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Environment') {
            steps {
                bat 'python --version'
                bat 'node --version'
                bat 'npm --version'
                bat 'git --version'
            }
        }

        stage('Backend Dependency Check') {
            steps {
                bat 'python -m venv .venv-ci'
                bat '.venv-ci\\Scripts\\python.exe -m pip install -r backend\\requirements.txt'
                bat '.venv-ci\\Scripts\\python.exe -m compileall -q backend'
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    bat 'npm ci'
                    bat 'npm run build'
                }
            }
        }
    }

    post {
        success {
            echo 'Samvaad CI pipeline completed successfully!'
        }

        failure {
            echo 'Samvaad CI pipeline failed. Check Console Output.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
