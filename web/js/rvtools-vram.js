import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
app.registerExtension({
    name: "memory.cleanup",
    init() {
        api.addEventListener("memory_cleanup", ({ detail }) => {
            if (detail.type === "cleanup_request") {
                console.log("Memory cleanup request received");
                fetch("/free", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(detail.data)
                })
                .then(response => {
                    if (response.ok) {
                        console.log("Memory cleanup request sent");
                    } else {
                        console.error("Memory cleanup request failed");
                    }
                })
                .catch(error => {
                    console.error("Error sending memory cleanup request:", error);
                });
            }
        });
    }
});
