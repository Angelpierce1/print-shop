class PrintShop < Formula
  desc "Print Shop - Image Quality Checker and HEIC/PDF Converter"
  homepage "https://github.com/yourusername/print-shop"
  url "https://github.com/yourusername/print-shop/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "YOUR_SHA256_HERE" # Replace with actual SHA256 after creating release
  license "MIT"
  version "1.0.0"
  
  depends_on "python@3.11"
  depends_on "poppler" # Required for PDF support
  
  def install
    python3 = Formula["python@3.11"].opt_bin/"python3.11"
    venv_root = libexec/"venv"
    
    # Create virtual environment
    system python3, "-m", "venv", venv_root
    
    # Install Python dependencies
    requirements = buildpath/"requirements.txt"
    system "#{venv_root}/bin/pip", "install", "-r", requirements
    
    # Install the application files
    libexec.install "app.py"
    libexec.install "convert_heic.py"
    libexec.install "init.py"
    
    # Create launcher script for main app
    (bin/"print-shop").write <<~EOS
      #!/bin/bash
      export PATH="#{Formula["poppler"].opt_bin}:$PATH"
      exec "#{venv_root}/bin/streamlit" run "#{libexec}/app.py" "$@"
    EOS
    
    # Create HEIC converter script
    (bin/"print-shop-convert-heic").write <<~EOS
      #!/bin/bash
      exec "#{venv_root}/bin/python3" "#{libexec}/convert_heic.py" "$@"
    EOS
    
    chmod 0755, bin/"print-shop"
    chmod 0755, bin/"print-shop-convert-heic"
  end
  
  test do
    # Test that the command exists and can show help
    system "#{bin}/print-shop", "--help"
  end
end

