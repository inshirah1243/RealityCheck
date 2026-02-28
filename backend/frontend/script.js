async function uploadVideo() {

    const file = document.getElementById("videoInput").files[0];

    if (!file) {
        alert("Please select a video.");
        return;
    }

    const uploadSection = document.getElementById("uploadSection");
    const loader = document.getElementById("loader");
    const results = document.getElementById("results");
    const bar = document.getElementById("confidenceBar");

    // Reset UI
    uploadSection.classList.add("hidden");
    loader.classList.remove("hidden");
    results.classList.add("hidden");
    bar.style.width = "0%";

    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch("http://127.0.0.1:8000/upload/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        loader.classList.add("hidden");
        results.classList.remove("hidden");

        // ===============================
        // Backend Fields
        // ===============================

        const fakeRatio = data.fake_ratio;
        const avgConfidence = data.average_confidence;
        const stability = data.stability_score;
        const faces = data.faces_analyzed;

        // 🔥 Your adjustment logic
        let fakePercent = ((fakeRatio * 100) - 0.20);

        // Prevent negative percentage
        if (fakePercent < 0) fakePercent = 0;

        fakePercent = fakePercent.toFixed(2);

        // ===============================
        // Populate UI
        // ===============================

        document.getElementById("confidenceText").innerText = fakePercent + "%";
        document.getElementById("stability").innerText = stability.toFixed(4);
        document.getElementById("facesAnalyzed").innerText = faces;
        document.getElementById("averageConfidence").innerText =
            (avgConfidence * 100).toFixed(2) + "%";

        // ===============================
        // Verdict Logic
        // ===============================

        const verdict = document.getElementById("verdict");

        if (fakeRatio > 0.65) {
            verdict.innerText = "🚨 High Risk - Likely Deepfake";
            bar.style.background = "#ef4444";
        }
        else if (fakeRatio > 0.40) {
            verdict.innerText = "⚠ Suspicious Content";
            bar.style.background = "#f59e0b";
        }
        else {
            verdict.innerText = "✅ Likely Real";
            bar.style.background = "#22c55e";
        }

        bar.style.width = fakePercent + "%";

        // ===============================
        // Download Report
        // ===============================

        const downloadBtn = document.getElementById("downloadBtn");

        if (downloadBtn) {

            downloadBtn.classList.remove("hidden");

            downloadBtn.onclick = function () {

                const report = {
                    faces_analyzed: faces,
                    fake_ratio: fakeRatio,
                    adjusted_percentage: fakePercent,
                    average_confidence: avgConfidence,
                    stability_score: stability
                };

                const blob = new Blob(
                    [JSON.stringify(report, null, 2)],
                    { type: "application/json" }
                );

                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "deepfake_analysis_report.json";
                a.click();
            };
        }

    } catch (error) {

        loader.classList.add("hidden");
        uploadSection.classList.remove("hidden");

        alert("Error analyzing video.");
        console.error(error);
    }
}