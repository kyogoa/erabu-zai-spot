async function initializeLiff() {
  const liffId = "{{ LIFF_ID }}";
  console.log("LIFF initialization started. LIFF ID:", liffId);

  // Flaskテンプレート外で使う場合に備えて、LIFF ID未設定でもフォーム確認は可能にする
  if (!window.liff || !liffId || liffId.includes("{{")) {
    console.warn("LIFF is not configured or not available.");
    return;
  }

  try {
    await liff.init({ liffId });
    console.log("LIFF initialized successfully.");

    if (!liff.isLoggedIn()) {
      console.log("Not logged in. Redirecting to login...");
      liff.login();
      return;
    }

    console.log("User is logged in. Getting profile...");
    const profile = await liff.getProfile();
    console.log("Profile retrieved:", profile);

    const lineUserIdInput = document.getElementById("line_user_id");
    const displayNameInput = document.getElementById("display_name");

    console.log("Setting form values...");
    if (lineUserIdInput) {
      lineUserIdInput.value = profile.userId;
      console.log("line_user_id set to:", profile.userId);
    } else {
      console.warn("line_user_id input not found");
    }

    if (displayNameInput) {
      displayNameInput.value = profile.displayName;
      console.log("display_name set to:", profile.displayName);
    } else {
      console.warn("display_name input not found");
    }

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
    console.log("LIFF link endpoint called successfully.");
  } catch (error) {
    console.error("LIFF initialization error:", error);
  }
}

initializeLiff().catch((error) => {
  console.error("LIFF initialization failed:", error);
});
