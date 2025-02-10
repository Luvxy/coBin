document.addEventListener('DOMContentLoaded', function () {
    const userId = "user123"; // 유저 ID (로그인 시 가져와야 함)

    // Firestore에서 데이터 가져오기
    db.collection("users").doc(userId).get().then((doc) => {
        if (doc.exists) {
            const user = doc.data();
            document.getElementById('userName').textContent = user.name;
            document.getElementById('userEmail').textContent = user.email;
            document.getElementById('membershipStatus').textContent = user.membership;

            if (user.profileImage) {
                document.getElementById('profileImage').src = user.profileImage;
            }
        } else {
            console.log("No such user document!");
        }
    }).catch((error) => {
        console.error("Error fetching user data:", error);
    });
});


// 프로필 편집 기능 (임시)
function editProfile() {
    const newName = prompt("Enter your new name:", document.getElementById('userName').textContent);
    if (newName) {
        document.getElementById('userName').textContent = newName;
    }

    const newEmail = prompt("Enter your new email:", document.getElementById('userEmail').textContent);
    if (newEmail) {
        document.getElementById('userEmail').textContent = newEmail;
    }
}

document.getElementById('imageUpload').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const userId = "user123"; // 유저 ID
    const storageRef = storage.ref(`profileImages/${userId}`);
    
    // 파일 업로드
    const uploadTask = storageRef.put(file);
    
    uploadTask.on("state_changed",
        (snapshot) => {
            // 업로드 진행 상태
            console.log(`Upload is ${(snapshot.bytesTransferred / snapshot.totalBytes) * 100}% done`);
        },
        (error) => {
            console.error("Upload failed:", error);
        },
        () => {
            // 업로드 완료 후 URL 가져와서 Firestore에 저장
            uploadTask.snapshot.ref.getDownloadURL().then((downloadURL) => {
                document.getElementById('profileImage').src = downloadURL;

                // Firestore에 이미지 URL 저장
                db.collection("users").doc(userId).update({
                    profileImage: downloadURL
                }).then(() => {
                    console.log("Profile image updated successfully!");
                }).catch((error) => {
                    console.error("Error updating profile image:", error);
                });
            });
        }
    );
});

function editProfile() {
    const userId = "user123"; // 유저 ID
    const newName = prompt("Enter your new name:", document.getElementById('userName').textContent);
    const newEmail = prompt("Enter your new email:", document.getElementById('userEmail').textContent);

    if (newName || newEmail) {
        db.collection("users").doc(userId).update({
            name: newName || document.getElementById('userName').textContent,
            email: newEmail || document.getElementById('userEmail').textContent
        }).then(() => {
            document.getElementById('userName').textContent = newName;
            document.getElementById('userEmail').textContent = newEmail;
            console.log("Profile updated successfully!");
        }).catch((error) => {
            console.error("Error updating profile:", error);
        });
    }
}
