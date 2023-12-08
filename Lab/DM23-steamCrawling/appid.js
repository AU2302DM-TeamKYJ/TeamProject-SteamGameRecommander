const fs = require("fs");
const appid = require("appid");

async function getGameNamesFromFile(filePath) {
    try {
        const fileContent = fs.readFileSync(filePath, "utf8");
        const gameIds = fileContent
            .split("\n")
            .map((line) => line.trim())
            .filter((line) => line)
            .slice(0, 10); // Only get the first 10 game IDs

        let gameMapping = [];

        for (let id of gameIds) {
            let gameName = await appid(parseInt(id));
            gameMapping.push({ id: id, name: gameName });
        }

        return gameMapping;
    } catch (err) {
        console.error("Error:", err);
    }
}

// getGameNamesFromFile("./data/appid_list.txt").then((mapping) => {
//     console.log("Game ID to Name Mapping:", mapping);
// });
