export function post(url, data, callback) {
  fetch(url, {
    body: JSON.stringify(data),
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow",
    referrerPolicy: "no-referrer",
  }).then((res) => res.json().then((data) => callback(data)));
}

export function get(url, callback, params = null) {
  let url_obj = new URL(url);
  if (params) {
    Object.keys(params).forEach((k) =>
      url_obj.searchParams.append(k, params[k])
    );
  }
  fetch(url_obj).then((res) => res.json().then((data) => callback(data)));
}

export function delete_request(url, callback) {
  fetch(url, {
    method: "DELETE",
  }).then(() => callback());
}
