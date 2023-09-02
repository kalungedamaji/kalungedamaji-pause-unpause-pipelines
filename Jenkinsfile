pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from your SCM
                checkout scm
            }
        }

        stage('Run Python Script') {
            steps {
                // Execute your Python script
                sh 'pip3 install -r requirements.txt'
                sh ' python3 run.py'
            }
        }
    }
}