pipeline {
    agent any

     parameters {
        string(name: 'JIRA_TICKET_NUMBER', description: 'Enter the Jira Ticket Number')
    }

     environment {
        // Define the credential ID for either SSH or PAT
         GIT_CREDENTIALS = "github-data-credentials"
    }

    stages {
               stage('Clean workspace') {
                    steps {
                       sh 'rm -rf *'
                    }
               }
               stage('Checkout Repos') {
                  steps {

                        dir('vitruvian--deployment-configurations') {
                            checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.gamesys.co.uk/Data/vitruvian-deployment-configurations', credentialsId: env.GIT_CREDENTIALS]]])
                        }

                         dir('pause_unpause_pipeline') {
                             checkout scm
                         }

                  }

                }

               stage('Run Python Script') {
                            steps {
                               script {
                                  def jira_ticket_number = params.JIRA_TICKET_NUMBER
                                  echo "jira_ticket_number ${jira_ticket_number}"
                                  dir('pause_unpause_pipeline') {

                                     sh 'pip3 install -r requirements.txt'
                                      sh ' python3 run.py'
                                  }
                              }
                            }
               }
    }
}