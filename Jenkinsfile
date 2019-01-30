pipeline {
    agent any
    triggers {
        pollSCM '* * * * *'
    }
    stages {
        stage('Build') {
            steps {
                sh '''
                    cd backend

                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt

                    mkdir -p instance
                    touch instance/config.py
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    cd backend
                    . venv/bin/activate
                    pytest
                '''
            }
        }
    }
}
