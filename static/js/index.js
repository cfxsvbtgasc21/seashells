/*from image_display.html*/

// 定义需要删除的文件路径列表
    const filesToDelete = { files_to_delete,tojson };

// 页面加载时，检查是否是刷新操作
window.addEventListener("load", function () {
    if (sessionStorage.getItem("isRefreshing")) {
        window.location.href = document.referrer || "/";
        sessionStorage.removeItem("isRefreshing");
    } else {
        window.addEventListener("beforeunload", function (e) {
            fetch("/delete_files", {
                method: "POST", headers: {
                    "Content-Type": "application/json",
                }, body: JSON.stringify({file_paths: filesToDelete}),
            })
                .then(response => response.json())
                .then(data => console.log("Files deleted:", data))
                .catch(error => console.error("Error deleting files:", error));
        });
    }
});

window.addEventListener("beforeunload", function () {
    sessionStorage.setItem("isRefreshing", "true");
});