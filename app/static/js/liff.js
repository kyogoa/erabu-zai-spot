async function initializeLiff() {
  const liffId = "{{ LIFF_ID }}";

  // Flaskテンプレート外で使う場合に備えて、LIFF ID未設定でもフォーム確認は可能にする
  if (!window.liff || !liffId || liffId.includes("{{")) {
    console.warn("LIFF is not configured.");
    return;
  }

  await liff.init({ liffId });

  if (!liff.isLoggedIn()) {
    liff.login();
    return;
  }

  const profile = await liff.getProfile();

  const lineUserIdInput = document.getElementById("line_user_id");
  const displayNameInput = document.getElementById("display_name");

  if (lineUserIdInput) lineUserIdInput.value = profile.userId;
  if (displayNameInput) displayNameInput.value = profile.displayName;

  await fetch("/link/liff", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      userId: profile.userId,
      displayName: profile.displayName,
      pictureUrl: profile.pictureUrl || "",
    }),
  });
}

initializeLiff().catch((error) => {
  console.error("LIFF initialization failed:", error);
});
