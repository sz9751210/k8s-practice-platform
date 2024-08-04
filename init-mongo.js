db = connect("mongodb://localhost:27017/it");

db.questions.insertMany([
  {
    type: "multiple-choice",
    question: "How many static pods exist in this cluster in all namespaces?",
    options: ["1", "3", "4", "2"],
    correctAnswer: 1
  },
  {
    type: "multiple-choice",
    question: "What is the default service type in Kubernetes?",
    options: ["ClusterIP", "NodePort", "LoadBalancer", "ExternalName"],
    correctAnswer: 0
  },
  {
    type: "confirmation",
    question: "Create an Nginx pod, with a count of 2.",
    checkInstructions: "Verify the number of Nginx pods running is 2.",
    commandTemplate: "kubectl get pods -l app={appName} --no-headers | wc -l",
    parameters: {
      appName: "nginx"
    },
    correctAnswer: "2"
  }
]);

print("Initial data inserted successfully");
