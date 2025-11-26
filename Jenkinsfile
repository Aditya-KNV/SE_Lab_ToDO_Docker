pipeline {
    agent any

    environment {
        IMAGE = "aditya8448/ci-cd-demo3:jenkins"
        VENV = ".venv"
        PYTHON = "/usr/bin/python3"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Aditya-KNV/SE_Lab_ToDO_Docker.git',
                        credentialsId: 'github-creds'
                    ]]
                ])
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh "${PYTHON} -m venv ${VENV}"
                sh "${VENV}/bin/pip install --upgrade pip"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh "${VENV}/bin/pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                sh "${VENV}/bin/pytest -v"
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                        echo $PASS | docker login -u $USER --password-stdin
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${IMAGE}"
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker pull ${IMAGE}
                    docker stop ci-cd-demo || true
                    docker rm ci-cd-demo || true
                    docker run -d -p 5000:5000 --name ci-cd-demo ${IMAGE}
                '''
            }
        }
    }
}
