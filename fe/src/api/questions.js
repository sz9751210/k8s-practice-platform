import httpClient from "@/utils/httpClient";

const host = "/api/devops";

export function fetchQuestions() {
  return httpClient({
    url: `${host}/questions`,
    method: "get",
    timeout: 10000,
  });
}

export function checkAnswer(data) {
  return httpClient({
    url: `${host}/check-answer`,
    method: "post",
    data,
    timeout: 10000,
  });
}