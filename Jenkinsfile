pipeline {
    agent any

    environment {
        DEPLOY_HOST = credentials('deploy-host')
        DEPLOY_USER = credentials('deploy-user')
        DEPLOY_PATH = '/opt/student-results'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt -r requirements-dev.txt'
                sh 'pytest -q'
            }
        }

        stage('Deploy') {
            steps {
                sshagent(credentials: ['deploy-ssh-key']) {
                    sh """
                        rsync -az --delete \
                          --exclude .git \
                          --exclude __pycache__ \
                          --exclude .pytest_cache \
                          --exclude .venv \
                          ./ ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}

                        ssh ${DEPLOY_USER}@${DEPLOY_HOST} \"cd ${DEPLOY_PATH} && docker compose up -d --build\"
                    """
                }
            }
        }
    }
}
