pipeline {
  agent any
  stages {
    stage('Init') {
      steps {
        withKubeConfig(contextName: 'c2.fra.k8scluster.de', credentialsId: '24d2e3c8-8b53-4333-99d4-62181446e589') {
          sh '''echo "Preparing environment ..."

echo "Checking for build-context"
if [ `kubectl get cm | grep context-input | wc -l` -eq 1 ]; then
  echo "Deleting build-context"
  kubectl delete cm context-input
fi

echo "Creating build-context"
kubectl create cm context-input --from-file=context/Dockerfile --from-file=context/sparkTest.py --from-file=context/requirements.txt
          
if [ `kubectl get job | grep kaniko | wc -l` -eq 1 ]; then
  kubectl delete job kaniko
fi
          
if [ `kubectl get job | grep bigdata | wc -l` -eq 1 ]; then
  kubectl delete job bigdata
fi

'''
        }

      }
    }
    stage('Build with Kaniko') {
      steps {
        withKubeConfig(contextName: 'c2.fra.k8scluster.de', credentialsId: '24d2e3c8-8b53-4333-99d4-62181446e589') {
          sh '''#!/bin/bash

echo "Configuring kaniko_job.yaml"
sed -i "s#--destination=index.docker.io/andperu/hello_world#--destination=index.docker.io/${DESTINATION}:${BUILD_NUMBER}#" kaniko_job.yaml
kubectl apply -f kaniko_job.yaml

while true; do
  kubectl get pod -a -l=job-name=kaniko
  STATE=`kubectl get pod -a -l=job-name=kaniko | tail -1 | awk \'{print $3}\'`
  if [ "$STATE" = "Completed" ]; then
    echo "Build done. Printing log"
    kubectl logs -l=job-name=kaniko
    break
  fi
  sleep 5
done

'''
        }

      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        withKubeConfig(credentialsId: '24d2e3c8-8b53-4333-99d4-62181446e589', contextName: 'c2.fra.k8scluster.de') {
          sh '''#!/bin/bash

echo "Preparing bigdata_job ..."
sed -i "s#andperu/spark:XXX#andperu/spark:${BUILD_NUMBER}#" bigdata_job.yaml
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
        withKubeConfig(contextName: 'c2.fra.k8scluster.de', credentialsId: '24d2e3c8-8b53-4333-99d4-62181446e589') {
          sh '''#!/bin/bash

kubectl logs -l=job-name=bigdata
kubectl delete job bigdata'''
        }

      }
    }
  }
  environment {
    DESTINATION = 'andperu/spark'
  }
}