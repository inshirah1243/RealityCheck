function injectButton() {

    // Only on watch pages
    if (!window.location.href.includes("watch")) return;

    // Prevent duplicates
    if (document.getElementById("realitycheck-btn")) return;

    // More reliable selector
    const titleContainer = document.querySelector("ytd-watch-metadata h1");

    if (!titleContainer) return;

    const btn = document.createElement("button");
    btn.id = "realitycheck-btn";
    btn.innerText = "Analyze with RealityCheck";

    btn.style.marginLeft = "12px";
    btn.style.padding = "6px 12px";
    btn.style.background = "#22c55e";
    btn.style.color = "white";
    btn.style.border = "none";
    btn.style.borderRadius = "6px";
    btn.style.cursor = "pointer";
    btn.style.fontWeight = "600";

    btn.onclick = async () => {

        btn.innerText = "Analyzing...";
        btn.disabled = true;

        try {

            const response = await fetch("http://127.0.0.1:8000/analyze_youtube/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: window.location.href })
            });

            const data = await response.json();

            if (data.error) {
                btn.innerText = "Error";
                btn.disabled = false;
                return;
            }

            const fakeRatio = data.fake_ratio;
            const fakePercent = ((fakeRatio * 100)-0.20).toFixed(2);

            let verdict;
            let color;

            if (fakeRatio > 0.85) {
                verdict = "🔴 Deepfake";
                color = "#ef4444";
            } 
            else if (fakeRatio > 0.75) {
                verdict = "🟡 Suspicious";
                color = "#f59e0b";
            } 
            else {
                verdict = "🟢 Real";
                color = "#22c55e";
            }

            btn.innerText = `${verdict} (${fakePercent}%)`;
            btn.style.background = color;

        } catch (err) {
            console.error(err);
            btn.innerText = "Failed";
            btn.disabled = false;
        }
    };

    titleContainer.appendChild(btn);
}


// Run initially
injectButton();

// YouTube dynamic navigation fix
const observer = new MutationObserver(() => {
    injectButton();
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});