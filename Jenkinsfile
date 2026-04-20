pipeline {
    agent any

    // Mencegah build yang sama berjalan dua kali di job yang sama
    // (tidak mempengaruhi job kelompok lain — mereka tetap bisa jalan bersamaan)
    options {
        disableConcurrentBuilds()
    }

    environment {
        SHORT_NAME     = "${JOB_NAME.split('/').last().toLowerCase()}"
        IMAGE_NAME     = "${SHORT_NAME}"
        IMAGE_TAG      = "${BUILD_NUMBER}"
        IMAGE_PREV_TAG = "${BUILD_NUMBER.toInteger() - 1}"
        CONTAINER_NAME = "${SHORT_NAME}-app"
        APP_PORT       = "8083"   // Ganti per kelompok: 8081 / 8082 / 8083 / 8084
    }

    stages {
        stage('Clone') {
            steps {
                // Otomatis clone dari SCM yang dikonfigurasi — tidak perlu hardcode URL
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ./app"
            }
        }

        stage('Test') {
            steps {
                sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m pytest /app/tests/ -v"
            }
        }

        stage('Deploy') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm   ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:5000 ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Cleanup') {
            steps {
                // Hanya hapus image LAMA milik job ini — tidak menyentuh image kelompok lain
                // yang mungkin sedang berjalan bersamaan
                script {
                    def prevTag = BUILD_NUMBER.toInteger() - 1
                    sh "docker rmi ${IMAGE_NAME}:${prevTag} || true"
                }
            }
        }
        stage('Health Check') {
            steps {
                script {
                    echo "Waiting for services to start..."
                    // Menunggu 10 detik agar Flask/Gunicorn benar-benar up
                    sleep 10
                    
                    echo "Checking endpoint health..."
                    try {
                        // -f: fail silently pada server error
                        // -s: silent mode (tidak menampilkan progress bar)
                        sh "curl -f -s http://localhost:${APP_PORT}/health || exit 1"
                        echo "Health check passed!"
                    } catch (Exception e) {
                        echo "Health check failed! Services might not be responding."
                        error "Deployment failed health check."
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deploy ${JOB_NAME} build #${BUILD_NUMBER} berhasil! Akses di port ${APP_PORT}"
        }
        failure {
            echo "❌ Build ${JOB_NAME} #${BUILD_NUMBER} gagal. Periksa log di atas."
            // Pastikan container lama tidak tertinggal jika deploy gagal di tengah jalan
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker rm   ${CONTAINER_NAME} || true"
        }
    }
}
