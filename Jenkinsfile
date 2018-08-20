pipeline {
  agent any
  stages {
    stage('Init') {
      steps {
        withKubeConfig(contextName: 'internal', credentialsId: '0026c120-8c5a-42d3-9b3c-2996408f9273') {
          sh '''echo "Preparing environment ..."

if [ `kubectl get cm | grep spark-code | wc -l` -eq 1 ]; then
  kubectl delete cm spark-code
fi

if [ `kubectl get job | grep bigdata | wc -l` -eq 1 ]; then
  kubectl delete job bigdata
fi

'''
        }

      }
    }
    stage('Build') {
      steps {
        withKubeConfig(contextName: 'internal', credentialsId: '0026c120-8c5a-42d3-9b3c-2996408f9273') {
          sh '''#!/bin/bash

echo "Create Spark application code"
kubectl create cm spark-code --from-file=sparkTest.py
kubectl get cm spark-code'''
        }

      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        withKubeConfig(credentialsId: '0026c120-8c5a-42d3-9b3c-2996408f9273', contextName: 'internal') {
          sh '''#!/bin/bash

kubectl apply -f bigdata_job.yaml

while true; do

  if [ `kubectl get pods -a -l=job-name=bigdata | grep -v \\^NAME | awk \'{print $3}\'` = "Completed" ]; then
    echo "Job finished "
    break
  else
    kubectl get pods -a -l=job-name=bigdata
    sleep 5
  fi

done '''
        }

      }
    }
    stage('Check Results') {
      steps {
        withKubeConfig(contextName: 'internal', credentialsId: '0026c120-8c5a-42d3-9b3c-2996408f9273') {
          sh '''#!/bin/bash

kubectl logs -l=job-name=bigdata
kubectl delete job bigdata'''
        }

      }
    }
  }
}
