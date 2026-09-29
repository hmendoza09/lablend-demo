pipeline {
    agent any

    environment {
        // Every build gets its own image tag, e.g. lablend/items-api:7
        TAG = "${env.BUILD_NUMBER}"
    }

    triggers {
        // Check GitHub for new commits every minute. No public URL needed.
        pollSCM('* * * * *')
    }

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                // Builds only the "test" stage of each Dockerfile, which runs pytest.
                // A failing test fails this stage, so Build and Deploy never run.
                sh 'docker build --target test -t lablend/items-api:test ./items-api'
                sh 'docker build --target test -t lablend/borrow-api:test ./borrow-api'
            }
        }

        stage('Build Images') {
            steps {
                // The real .env is stored in Jenkins Credentials, not in Git
                withCredentials([file(credentialsId: 'lablend-env', variable: 'ENV_FILE')]) {
                    sh 'cp "$ENV_FILE" .env'
                }
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                // Replaces running containers with the new build; the db-data volume is kept
                sh 'docker compose up -d --no-build --remove-orphans'
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                  for i in $(seq 1 20); do
                    if docker compose exec -T proxy wget -qO- http://127.0.0.1/api/items/health >/dev/null 2>&1 \
                       && docker compose exec -T proxy wget -qO- http://127.0.0.1/api/borrows/health >/dev/null 2>&1 \
                       && docker compose exec -T proxy wget -qO- http://127.0.0.1/ | grep -q "Build ${TAG}"; then
                      echo "Smoke test passed: build ${TAG} is live"
                      exit 0
                    fi
                    echo "Waiting for services... attempt $i"
                    sleep 5
                  done
                  echo "Smoke test FAILED"
                  docker compose ps
                  exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "LabLend build ${TAG} is live at http://127.0.0.1:8080"
        }
        failure {
            echo "Build ${TAG} failed. The previous version is still running if the failure happened before Deploy."
            echo "Manual rollback: TAG=<previous build> docker compose up -d --no-build"
        }
        always {
            sh 'rm -f .env'   // never leave the secret file lying in the workspace
        }
    }
}
