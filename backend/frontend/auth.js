const token = sessionStorage.getItem("token");

if (!token) {
    window.location.href = "/frontend/index.html";
} else {
    fetch("/auth/verify-token", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => {
        if (!res.ok) {
            sessionStorage.removeItem("token");
            window.location.href = "/frontend/index.html";
        }
    })
    .catch(() => {
        sessionStorage.removeItem("token");
        window.location.href = "/frontend/index.html";
    });
}
