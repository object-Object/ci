const fs = require("fs");
const core = require("@actions/core");

function main() {
    const path = core.getInput("file");
    const data = JSON.parse(fs.readFileSync(path));

    const keys = Object.keys(data);
    if (keys.length !== 1) {
        core.setFailed(
            `Expected exactly 1 stack, but got ${keys.length}: ${keys.join()}`
        );
        return;
    }

    const stackName = keys[0];
    core.info(`Stack name: ${stackName}`);
    core.setOutput("stack-name", stackName);

    core.info("Stack outputs:");
    for (const [key, value] of Object.entries(data[stackName])) {
        core.info(`  ${key} = ${value}`);
        core.setOutput(key, value);
    }
}

try {
    main();
} catch (error) {
    core.setFailed(error.message);
}
