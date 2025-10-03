import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "RvTools-X.appearance",
        nodeCreated(node) {
            node.color = "#4e4e4e";
            node.bgcolor = "#3a3a3a";
            node.shape = "box";
        }
});
