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
           script {
            def targetEnv = params.JIRA_TICKET_NUMBER
                echo " Jira Ticket ${targetEnv}"
           }
            steps {
                // Execute your Python script

                sh 'pip3 install -r requirements.txt'
                sh ' python3 run.py'
            }
        }
    }
}