import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Dracula theme colors
BG_COLOR = '#282a36'  # Dark background
FG_COLOR = '#f8f8f2'  # Light foreground text
PURPLE   = '#BD93F9'  # Primary color
ORANGE   = '#FFB86C'  # Secondary color
PINK     = '#FF79C6'  # Tertiary color
GREEN    = '#50FA7B'  # Additional color
CYAN     = '#8BE9FD'  # Additional color

plt.rcParams.update(
    {
        "figure.facecolor": BG_COLOR,
        "axes.facecolor"  : BG_COLOR,
        "axes.edgecolor"  : FG_COLOR,
        "axes.labelcolor" : FG_COLOR,
        "xtick.color"     : FG_COLOR,
        "ytick.color"     : FG_COLOR,
        "text.color"      : FG_COLOR,
        "axes.prop_cycle" : plt.cycler(color=[PURPLE, ORANGE, PINK, CYAN, GREEN]),
        "grid.color"      : FG_COLOR,
        "grid.alpha"      : 0.3,
        "grid.linestyle"  : "--",
    }
)

def style_axes(ax, edgecolor=FG_COLOR, linewidth=1.2):
    ax.set_facecolor(BG_COLOR)
    ax.tick_params(colors=FG_COLOR)
    for spine in ax.spines.values():
        spine.set_color(FG_COLOR)
    for patch in ax.patches:
        if hasattr(patch, "get_facecolor"):
            face = patch.get_facecolor()
            patch.set_edgecolor(edgecolor or face)
            patch.set_linewidth(linewidth)

def box_muller():
    """Box-Muller transform to convert uniform random variables to normal"""
    u1 = np.random.uniform(0, 1)
    u2 = np.random.uniform(0, 1)
    z1 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    z2 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
    return z1, z2

def generate_samples(n_samples=10000):
    """Generate samples using Box-Muller transform"""
    u1_samples = []
    u2_samples = []
    z1_samples = []
    z2_samples = []
    
    for _ in range(n_samples):
        u1 = np.random.uniform(0, 1)
        u2 = np.random.uniform(0, 1)
        z1 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        z2 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
        
        u1_samples.append(u1)
        u2_samples.append(u2)
        z1_samples.append(z1)
        z2_samples.append(z2)
    
    return np.array(u1_samples), np.array(u2_samples), np.array(z1_samples), np.array(z2_samples)

def create_visualization():
    """Create comprehensive Box-Muller visualization"""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate samples
    n_samples = 10000
    u1, u2, z1, z2 = generate_samples(n_samples)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # Create a 3x3 grid for comprehensive visualization
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Input uniform distributions
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(u1, bins=50, alpha=0.7, color=PURPLE, edgecolor=FG_COLOR, linewidth=0.8)
    ax1.axhline(y=n_samples/50, color=ORANGE, linestyle='--', linewidth=2, 
                label='Theoretical uniform')
    ax1.set_title('Input U1 ~ Uniform(0,1)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    ax1.grid(True)
    style_axes(ax1)
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.hist(u2, bins=50, alpha=0.7, color=PINK, edgecolor=FG_COLOR, linewidth=0.8)
    ax2.axhline(y=n_samples/50, color=ORANGE, linestyle='--', linewidth=2,
                label='Theoretical uniform')
    ax2.set_title('Input U2 ~ Uniform(0,1)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Value')
    ax2.set_ylabel('Frequency')
    ax2.legend()
    ax2.grid(True)
    style_axes(ax2)
    
    # 2. 2D scatter of uniform inputs
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.scatter(u1[:1000], u2[:1000], alpha=0.6, s=10, color=CYAN)
    ax3.set_title('Joint Distribution of U1, U2', fontsize=12, fontweight='bold')
    ax3.set_xlabel('U1')
    ax3.set_ylabel('U2')
    ax3.grid(True)
    style_axes(ax3)
    
    # 3. Output normal distributions
    ax4 = fig.add_subplot(gs[1, 0])
    n, bins, patches = ax4.hist(z1, bins=50, alpha=0.7, color=GREEN, 
                                edgecolor=FG_COLOR, linewidth=0.8, density=True)
    # Overlay theoretical normal distribution
    x = np.linspace(-4, 4, 100)
    y = stats.norm.pdf(x, 0, 1)
    ax4.plot(x, y, color=ORANGE, linewidth=3, label='Theoretical N(0,1)')
    ax4.set_title('Output Z1 ~ Normal(0,1)', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Value')
    ax4.set_ylabel('Density')
    ax4.legend()
    ax4.grid(True)
    style_axes(ax4)
    
    ax5 = fig.add_subplot(gs[1, 1])
    n, bins, patches = ax5.hist(z2, bins=50, alpha=0.7, color=CYAN, 
                                edgecolor=FG_COLOR, linewidth=0.8, density=True)
    ax5.plot(x, y, color=ORANGE, linewidth=3, label='Theoretical N(0,1)')
    ax5.set_title('Output Z2 ~ Normal(0,1)', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Value')
    ax5.set_ylabel('Density')
    ax5.legend()
    ax5.grid(True)
    style_axes(ax5)
    
    # 4. 2D scatter of normal outputs
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.scatter(z1[:1000], z2[:1000], alpha=0.6, s=10, color=PURPLE)
    ax6.set_title('Joint Distribution of Z1, Z2', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Z1')
    ax6.set_ylabel('Z2')
    ax6.grid(True)
    style_axes(ax6)
    
    # 5. Q-Q plots for normality check
    ax7 = fig.add_subplot(gs[2, 0])
    stats.probplot(z1, dist="norm", plot=ax7)
    ax7.get_lines()[0].set_markerfacecolor(GREEN)
    ax7.get_lines()[0].set_markeredgecolor(FG_COLOR)
    ax7.get_lines()[1].set_color(ORANGE)
    ax7.get_lines()[1].set_linewidth(2)
    ax7.set_title('Q-Q Plot: Z1 vs Normal', fontsize=12, fontweight='bold')
    ax7.grid(True)
    style_axes(ax7)
    
    ax8 = fig.add_subplot(gs[2, 1])
    stats.probplot(z2, dist="norm", plot=ax8)
    ax8.get_lines()[0].set_markerfacecolor(CYAN)
    ax8.get_lines()[0].set_markeredgecolor(FG_COLOR)
    ax8.get_lines()[1].set_color(ORANGE)
    ax8.get_lines()[1].set_linewidth(2)
    ax8.set_title('Q-Q Plot: Z2 vs Normal', fontsize=12, fontweight='bold')
    ax8.grid(True)
    style_axes(ax8)
    
    # 6. Statistical summary
    ax9 = fig.add_subplot(gs[2, 2])
    ax9.axis('off')
    
    # Calculate statistics
    z1_mean, z1_std = np.mean(z1), np.std(z1, ddof=1)
    z2_mean, z2_std = np.mean(z2), np.std(z2, ddof=1)
    
    stats_text = f"""
    Statistical Summary (n={n_samples:,})
    
    Z1 Statistics:
    Mean: {z1_mean:.4f} (theoretical: 0.0000)
    Std:  {z1_std:.4f} (theoretical: 1.0000)
    
    Z2 Statistics:
    Mean: {z2_mean:.4f} (theoretical: 0.0000)
    Std:  {z2_std:.4f} (theoretical: 1.0000)
    
    Correlation(Z1, Z2): {np.corrcoef(z1, z2)[0,1]:.4f}
    (theoretical: 0.0000)
    
    Box-Muller Transform:
    Z1 = √(-2ln(U1)) × cos(2πU2)
    Z2 = √(-2ln(U1)) × sin(2πU2)
    """
    
    ax9.text(0.05, 0.95, stats_text, transform=ax9.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor=BG_COLOR, edgecolor=FG_COLOR, alpha=0.8))
    
    # Main title
    fig.suptitle('Box-Muller Transform: Converting Uniform to Normal Distributions', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    create_visualization()