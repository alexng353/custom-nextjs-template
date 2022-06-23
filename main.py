import os, sys, webbrowser

# read cli args and set variables
args = sys.argv[1:]
if len(args) == 0:
    print("No arguments given")
    sys.exit(1)
if "--ts" in args:
    ts = True
else:
    ts = False
if "--name" in args:
    # find the index of the --name argument
    name = args[args.index("--name")+1]
    # replace all spaces with underscores
    if name.strip() == "":
        print("No name given")
        sys.exit(1)
    name = name.replace(" ", "_")
    
else:
    name = input("Name:\n>>>")
if "--dev" in args:
    dev = True
    if "--port" in args:
        port = args[args.index("--dev")+1]
    else:
        port = input("Port:\n>>>")
        if not port.isnumeric():
            raise Exception("Port must be a number")
        if int(port) < 1024 or int(port) > 65535:
            raise Exception("Port must be between 1024 and 65535")
        if port == "":
            raise Exception("Port must be a number")
else:
    dev = False
if "--nobrowser" in args:
    nobrowser = True



tailwind = True if "--tailwind" in args else False
mui = True if "--mui" in args else False

tailwind_config_js = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}"""

globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;"""

index_page = """import type { NextPage } from 'next'
import Head from 'next/head'

const Home: NextPage = () => {
  return (
    <div>
      <Head>
        <title>Create Next MUI TailwindCSS App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div>
        <a href="https://nextjs.org" style={{color:"blue", textDecoration:"underline"}} target="blank">Learn Next.js</a>
        <br/>
        <a href="https://mui.com" style={{color:"blue", textDecoration:"underline"}}>Learn MaterialUI</a>
        <br/>
        <a href="https://tailwindcss.com" style={{color:"blue", textDecoration:"underline", }}>Learn TailwindCSS</a>
      </div>
    </div>
  )
}

export default Home"""

os.system(f'npx create-next-app@latest {name} {"--ts" if ts else ""}')
os.system(f'cd {name}')
if tailwind:
    os.system(f'cd {name} && npm install -D tailwindcss postcss autoprefixer')
    os.system(f'cd {name} && npx tailwindcss init -p')
    f = open(f"{name}/tailwind.config.js", "w")
    f.write(tailwind_config_js)
    f.close()
    g = open(f"{name}/styles/globals.css", "w")
    g.write(globals_css)
    g.close()
    os.system(f'rm {name}/styles/Home.module.css')
    os.system(f'rm {name}/pages/index.{"tsx" if ts else "js"}')
    h = open(f"{name}/pages/index.{'tsx' if ts else 'js'}", "w")
    h.write(index_page)
    h.close()
    
if mui:
    os.system(f'cd {name} && npm install @mui/material @emotion/react @emotion/styled')

if dev:
    os.system(f'cd {name} && npm run dev {"-- -p " + port if port else ""}')
    if not nobrowser:
        webbrowser.open(f"http://localhost:{port}")