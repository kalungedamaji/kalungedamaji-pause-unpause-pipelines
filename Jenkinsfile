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
              script {
            def targetEnv = params.JIRA_TICKET_NUMBER
                echo " Jira Ticket ${targetEnv}"
           }
              def currentDir = pwd()

                    // Navigate to the previous directory
                    dir(currentDir) {
                  sh 'ls '
                  sh 'pwd '
                }
                sh 'pip3 install -r requirements.txt'
                sh ' python3 run.py'
            }
        }
    }
}