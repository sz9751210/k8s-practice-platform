import httpClient from "@/utils/httpClient";

const host = "/api/devops/k8s";

export function resetK8s() {
  return httpClient({
    url: `${host}/reset`,
    method: "post",
    timeout: 300000
  });
}
