document.addEventListener("DOMContentLoaded", function () {
    const terminal = new Terminal();
    terminal.open(document.getElementById("terminal"));

    terminal.writeln("Welcome to the Linux PlayGround!");
    terminal.prompt = () => {
        terminal.write("\r\n$ ");
    };

    terminal.onKey((e) => {
        const command = e.key;
        if (command === "Enter") {
            // Execute the command via Flask API
            fetch(`/execute/${terminal.inputBuffer}`)
                .then((response) => response.text())
                .then((output) => {
                    terminal.writeln(output);
                    terminal.prompt();
                });
        } else {
            terminal.inputBuffer += command;
        }
    });

    terminal.prompt();
});
