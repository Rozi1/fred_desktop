
### 📋 Prerequisites

- Python >=3.8.0
- An OpenAI API key that can access OpenAI API (set up a paid account OpenAI account)
- Windows OS (Not tested on others)
- FFmpeg 

If FFmpeg is not installed in your system, you can follow the steps below to install it.

First, you need to install Chocolatey, a package manager for Windows. Open your PowerShell as Administrator and run the following command:
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
Once Chocolatey is installed, you can install FFmpeg by running the following command in your PowerShell:
```
choco install ffmpeg
```
Please ensure that you run these commands in a PowerShell window with administrator privileges. If you face any issues during the installation, you can visit the official Chocolatey and FFmpeg websites for troubleshooting.

### 🔧 Installation

1. Clone the repository:

   ```
   git clone https://github.com/Hiramgm/Fred-Speech-to-Text.git
   ```

2. Navigate to the `Fred-Speech-to-Text` folder:

   ```
   cd Fred-Speech-to-Text
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```
   
4. Create a `keys.py` file in the Fred-Speech-to-Text directory and add your OpenAI API key:

   - Option 1: You can utilize a command on your command prompt. Run the following command, ensuring to replace "API KEY" with your actual OpenAI API key:

      ```
      python -c "with open('keys.py', 'w', encoding='utf-8') as f: f.write('OPENAI_API_KEY=\"API KEY\"')"
      ```

   - Option 2: You can create the keys.py file manually. Open up your text editor of choice and enter the following content:
   
      ```
      OPENAI_API_KEY="API KEY"
      ```
      Replace "API KEY" with your actual OpenAI API key. Save this file as keys.py within the Fred-Speech-to-Text directory.

### 🎬 Running Fred-Speech-to-Text

Run the main script:

```
python main.py
```

For a more better and faster version that also works with most languages, use:

```
python main.py --api
```




