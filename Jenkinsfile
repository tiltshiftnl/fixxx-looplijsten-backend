#!groovy

def push_image(tag) {
  script {
    def image = docker.image("${env.DOCKER_REGISTRY}/${env.DOCKER_IMAGE}:${env.COMMIT_HASH}")
    image.push(tag)
  }
}

def deploy(environment) {
  build job: 'Subtask_Openstack_Playbook',
    parameters: [
        [$class: 'StringParameterValue', name: 'INFRASTRUCTURE', value: 'secure'],
        [$class: 'StringParameterValue', name: 'INVENTORY', value: acceptance],
        [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-looplijsten-backend.yml'],
    ]
}

pipeline {
  agent any
  environment {
    DOCKER_IMAGE = "fixxx/looplijsten"
    APP = "looplijsten-api"
    DOCKER_REGISTRY = "repo.secure.amsterdam.nl"
  }

  stages {
    stage("Checkout") {
      steps {
        checkout scm
        script {
          env.COMMIT_HASH = sh(returnStdout: true, script: "git log -n 1 --pretty=format:'%h'").trim()
        }
      }
    }

    // stage("Run tests") {
    //   steps {
    //     script {
    //       sh "docker-compose run --rm api python manage.py test"
    //       sh "docker-compose down --rmi local || true"
    //     }
    //   }
    // }

    stage("Build docker image") {
      // We only build a docker image when we're not deploying to production,
      // to make make sure images deployed to production are deployed to
      // acceptance first.
      //
      // To deploy to production, tag an existing commit (that has already been
      // build) and push the tag.
      // (looplijsten actually wants to be able to hotfix to production,
      // without passing through acceptance)
      //when { not { buildingTag() } }

      steps {
        script {
          def image = docker.build("${env.DOCKER_REGISTRY}/${env.DOCKER_IMAGE}:${env.COMMIT_HASH}",
            "--no-cache " +
            "--shm-size 1G " +
            " ./app")
          image.push()
          image.push("latest")
        }
      }
    }

    stage("Push and deploy acceptance image") {
      when {
        not { buildingTag() }
        branch 'master'
      }
      steps {
        push_image("acceptance")
        deploy("acceptance")
      }
    }

    stage("Push and deploy production image") {
      when { buildingTag() }
      steps {
        push_image("production")
        push_image(env.TAG_NAME)
        deploy("production")
      }
    }

  }
}
