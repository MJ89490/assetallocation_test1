pipeline {
  agent { docker { image 'python:3.6.5' } }
    triggers {
        pollSCM('*/5 * * * 1-5')
    }
    options {
        skipDefaultCheckout(true)
        // Keep the 10 most recent builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    environment {
      PATH="<python_path>:$PATH"
    }

    stages {
        stage ("Code pull"){
            steps{
                checkout scm
            }
        }
        stage('Build environment') {
            steps {
                sh '''env ${BUILD_TAG}
                      source activate ${BUILD_TAG}
                      pip install -r requirements.txt
                    '''
            }
        }
        stage('Test environment') {
            steps {
                sh '''source activate ${BUILD_TAG}
                       pytest tests --doctest-modules --junitxml=junit/test-results.xml --cov --cov-report=xml --cov-report=html
                    '''
            }
        }
        stage('Check sonarcube') {
            steps {
                sh '''env ${BUILD_TAG}
                      source activate ${BUILD_TAG}
                      sonar-scanner
                    '''
            }
        }
    }
    post {
        failure {
            echo "Send e-mail, when failed"
        }
    }
}