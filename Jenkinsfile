pipeline {
    agent any

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
                stage('Checkout deployment-configurations') {
                  steps {

                        dir('vitruvian_deployment_configurations') {
                            checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.gamesys.co.uk/Data/vitruvian-deployment-configurations', credentialsId: env.GIT_CREDENTIALS]]])
                        }
                  }

                }

                 stage('Checkout pause unpause repo') {
                        steps {

                           dir('pause_unpause_pipeline') {
                             checkout scm
                             }
                        }
                 }

                 stage('Run Python Script') {

                        steps {
                              dir('pause_unpause_pipeline') {

                                 sh 'pip3 install -r requirements.txt'
                                sh ' python3 run.py'
                              }
                        }
                 }
    }
}