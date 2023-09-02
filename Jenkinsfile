pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from your SCM
                checkout scm
                checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.gamesys.co.uk/Data/vitruvian-deployment-configurations']]])

            }
        }

        stage('Run Python Script') {

            steps {
             script {
                    // Get the paths of the checked-out repositories
                    sh 'ls'
                    sh 'pwd'
                    sh 'cd ..'
                     sh 'ls'
                    sh 'pwd'
                    def repo1Path = pwd() // Path of the first repository
                    def repo2Path = "${pwd()}/../vitruvian-deployment-configurations" // Path of the second repository

                    echo "Path of Repository 1: ${repo1Path}"
                    echo "Path of Repository 2: ${repo2Path}"
                }

                sh 'pip3 install -r requirements.txt'
                sh ' python3 run.py'
            }
        }
    }
}