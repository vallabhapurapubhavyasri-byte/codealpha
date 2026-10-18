/**
 * StyleCart - Client-Side Interactive Enhancements
 * Beginner-friendly JavaScript for smooth user experience.
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-dismiss flash alert messages after 4.5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Use Bootstrap's alert dismiss if available
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                // Fallback fade out
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 4500);
    });

    // 2. Quantity Input validation on Product Details page
    const quantityInput = document.getElementById('quantity');
    if (quantityInput) {
        quantityInput.addEventListener('change', function () {
            const min = parseInt(this.min, 10) || 1;
            const max = parseInt(this.max, 10) || 999;
            let val = parseInt(this.value, 10);

            if (isNaN(val) || val < min) {
                this.value = min;
            } else if (val > max) {
                this.value = max;
                alert(`Maximum available stock is ${max} units.`);
            }
        });
    }

    // 3. Smooth card image error fallback
    const images = document.querySelectorAll('img');
    images.forEach(function (img) {
        img.addEventListener('error', function () {
            this.src = 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60';
        });
    });
});
