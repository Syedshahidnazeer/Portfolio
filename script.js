const roleItems = document.querySelectorAll('.role-item');

roleItems.forEach(item => {
    item.addEventListener('click', function() {
        const role = this.dataset.role;
        // Communicate the selected role to your Streamlit app (example using session state)
        // You'll need to adapt this based on how you're handling role selection
        sessionStorage.setItem('selectedRole', role); 
    });
});