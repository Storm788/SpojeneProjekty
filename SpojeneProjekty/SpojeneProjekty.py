import sqlite3
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

NAZEV_DATABAZE = "Pro3.db"

def nacti_otazky_z_databaze():
    otazky = []
    conn = sqlite3.connect(NAZEV_DATABAZE)
    cursor = conn.cursor()
    cursor.execute("SELECT Otazka, Odpoved1, Odpoved2, Odpoved3, Odpoved4, SpravnaOd FROM Quiz")
    
    for radek in cursor.fetchall():
        otazky.append({
            "otazka": radek[0],
            "moznosti": [radek[1], radek[2], radek[3], radek[4]],
            "spravna_moznost": int(radek[5])  # Převedení na index (0-based)
        })
    
    conn.close()
    return otazky

class QuizServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html_content = """
                <html>
                <body>
                    <h1>Vitejte v KVÍZU</h1>
                    <button onclick="startQuiz()">Zahájit kvíz</button>
                    <div id="quizContainer" style="display:none;"></div>
                    <script>
                        function startQuiz() {
                            fetch('/otazky')
                                .then(response => response.json())
                                .then(data => {
                                    let quizHtml = '<form id="quizForm">';
                                    data.forEach((q, index) => {
                                        quizHtml += `<p>${q.otazka}</p>`;
                                        q.moznosti.forEach((moznost, i) => {
                                            quizHtml += `<input type='radio' name='otazka${index}' value='${i}'> ${moznost}<br>`;
                                        });
                                    });
                                    quizHtml += '<button type="button" onclick="submitQuiz()">Odeslat</button></form>';
                                    document.getElementById('quizContainer').innerHTML = quizHtml;
                                    document.getElementById('quizContainer').style.display = 'block';
                                })
                                .catch(error => console.error('Chyba při načítání otázek:', error));
                        }
                        
                        function submitQuiz() {
                            let odpovedi = [];
                            document.querySelectorAll('form input[type=radio]:checked').forEach(input => {
                                odpovedi.push(Number(input.value));
                            });
                            fetch('/vyhodnotit', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ odpovedi })
                            })
                            .then(response => response.json())
                            .then(data => {
                                alert(`Kvíz dokončen! Výsledek: ${data.skore} z ${data.celkem}`);
                            })
                            .catch(error => console.error('Chyba při odesílání odpovědí:', error));
                        }
                    </script>
                </body>
                </html>
            """
            self.wfile.write(html_content.encode("utf-8"))
        elif self.path == '/otazky':
            otazky = nacti_otazky_z_databaze()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(otazky).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/vyhodnotit':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            otazky = nacti_otazky_z_databaze()
            
            skore = 0
            for i, odp in enumerate(post_data.get("odpovedi", [])):
                if i < len(otazky):
                    spravna_moznost = otazky[i]["spravna_moznost"]
                    print(f"Spravná možnost je pro {i}--> {spravna_moznost + 1}")
                    if odp == spravna_moznost:
                        skore += 1
            vysledek = {"skore": skore, "celkem": len(otazky)}
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(vysledek).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server_address = ('', 1000)
    httpd = HTTPServer(server_address, QuizServer)
    print("Server běží na portu 1000...")
    httpd.serve_forever()
