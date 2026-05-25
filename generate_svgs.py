import os

OUT = "/Users/eunhuismacbook/Desktop/hanigame/images"
os.makedirs(OUT, exist_ok=True)

SK = "#FDBCB4"  # skin
HR = "#2C1A0E"  # hair

def HEAD(cx, cy, skin=SK, hair=HR):
    return f"""
  <circle cx="{cx}" cy="{cy}" r="40" fill="{skin}"/>
  <ellipse cx="{cx}" cy="{cy-20}" rx="36" ry="22" fill="{hair}"/>
  <circle cx="{cx-40}" cy="{cy}" r="10" fill="{skin}"/>
  <circle cx="{cx+40}" cy="{cy}" r="10" fill="{skin}"/>
  <circle cx="{cx-13}" cy="{cy+2}" r="8" fill="white"/>
  <circle cx="{cx+13}" cy="{cy+2}" r="8" fill="white"/>
  <circle cx="{cx-12}" cy="{cy+3}" r="5" fill="#222"/>
  <circle cx="{cx+14}" cy="{cy+3}" r="5" fill="#222"/>
  <circle cx="{cx-12}" cy="{cy+3}" r="2.5" fill="#4A90D9"/>
  <circle cx="{cx+14}" cy="{cy+3}" r="2.5" fill="#4A90D9"/>
  <circle cx="{cx-12}" cy="{cy+3}" r="1.5" fill="#111"/>
  <circle cx="{cx+14}" cy="{cy+3}" r="1.5" fill="#111"/>
  <circle cx="{cx-10}" cy="{cy+1}" r="1.3" fill="white"/>
  <circle cx="{cx+16}" cy="{cy+1}" r="1.3" fill="white"/>
  <ellipse cx="{cx}" cy="{cy+12}" rx="3.5" ry="2.5" fill="#F08070"/>
  <path d="M {cx-13} {cy+17} Q {cx} {cy+28} {cx+13} {cy+17}" stroke="#C1440E" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <circle cx="{cx-19}" cy="{cy+14}" r="8" fill="rgba(255,120,90,0.22)"/>
  <circle cx="{cx+19}" cy="{cy+14}" r="8" fill="rgba(255,120,90,0.22)"/>"""

def BODY(cx, cy, col, w=66, h=52):
    return f'  <rect x="{cx-w//2}" y="{cy}" width="{w}" height="{h}" rx="13" fill="{col}"/>\n'

def ARM_L(cx, cy, col):
    return f'  <rect x="{cx-w}" y="{cy}" width="32" height="14" rx="7" fill="{col}"/>\n'.replace(
        '{cx-w}', str(cx-94)).replace('{cy}', str(cy))

def LEGS(cx, cy, col, shoe="#333"):
    return f"""
  <rect x="{cx-28}" y="{cy}" width="22" height="20" rx="8" fill="{col}"/>
  <rect x="{cx+6}" y="{cy}" width="22" height="20" rx="8" fill="{col}"/>
  <ellipse cx="{cx-17}" cy="{cy+20}" rx="13" ry="6" fill="{shoe}"/>
  <ellipse cx="{cx+17}" cy="{cy+20}" rx="13" ry="6" fill="{shoe}"/>"""

def SHADOW(cx, cy):
    return f'  <ellipse cx="{cx}" cy="{cy}" rx="52" ry="9" fill="rgba(0,0,0,0.10)"/>\n'

def BG(c1, c2):
    return f"""  <defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{c1}"/>
    <stop offset="100%" stop-color="{c2}"/>
  </linearGradient></defs>
  <rect width="240" height="240" fill="url(#bg)"/>"""

def WRAP(inner):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">\n{inner}\n</svg>'

# ─── Scene builders ────────────────────────────────────────────────────────────

def s01_hello():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#B0E0FF","#E0F7FA")}
{SHADOW(120,228)}
{h}
  <!-- school uniform blue -->
  <rect x="87" y="148" width="66" height="52" rx="13" fill="#3F51B5"/>
  <path d="M 105 148 L 120 160 L 135 148" fill="white" opacity="0.6"/>
  <!-- left arm normal -->
  <rect x="54" y="148" width="35" height="14" rx="7" fill="#3F51B5"/>
  <circle cx="51" cy="151" r="11" fill="{SK}"/>
  <!-- right arm raised -->
  <rect x="167" y="122" width="14" height="34" rx="7" fill="#3F51B5"/>
  <circle cx="173" cy="118" r="11" fill="{SK}"/>
  <!-- wave lines -->
  <path d="M 179 106 Q 192 100 185 91" stroke="#FFD700" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M 187 112 Q 200 105 193 96" stroke="#FFD700" stroke-width="2" fill="none" stroke-linecap="round"/>
{LEGS(120,196,"#3F51B5")}
  <!-- confetti -->
  <rect x="32" y="26" width="9" height="6" rx="2" fill="#FF6B6B" transform="rotate(-20 32 26)"/>
  <rect x="188" y="38" width="8" height="6" rx="2" fill="#FFD700" transform="rotate(15 188 38)"/>
  <rect x="55" y="50" width="7" height="5" rx="2" fill="#69F0AE" transform="rotate(30 55 50)"/>
  <rect x="196" y="72" width="9" height="6" rx="2" fill="#FF8CE8" transform="rotate(-10 196 72)"/>
  <circle cx="170" cy="30" r="5" fill="#FF8CE8"/>
  <circle cx="28" cy="65" r="4" fill="#FFD700"/>
  <circle cx="212" cy="50" r="5" fill="#69F0AE"/>
""")

def s02_my_name():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#FFF9C4","#FFFDE7")}
{SHADOW(120,228)}
{h}
  <!-- body yellow -->
  <rect x="87" y="148" width="66" height="52" rx="13" fill="#FFA000"/>
  <!-- right arm pointing to self -->
  <rect x="54" y="155" width="36" height="14" rx="7" fill="#FFA000"/>
  <circle cx="50" cy="158" r="11" fill="{SK}"/>
  <!-- left arm normal -->
  <rect x="151" y="148" width="35" height="14" rx="7" fill="#FFA000"/>
  <circle cx="189" cy="152" r="11" fill="{SK}"/>
  <!-- name badge on chest -->
  <rect x="97" y="158" width="46" height="28" rx="6" fill="white" stroke="#FFD700" stroke-width="2"/>
  <circle cx="120" cy="152" r="4" fill="#FFD700"/>
  <!-- star on badge -->
  <polygon points="120,164 122.5,171 130,171 124,175.5 126.5,182.5 120,178 113.5,182.5 116,175.5 110,171 117.5,171" fill="#FFD700"/>
{LEGS(120,196,"#FFA000")}
  <!-- sparkles -->
  <line x1="35" y1="50" x2="35" y2="62" stroke="#FFD700" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="29" y1="56" x2="41" y2="56" stroke="#FFD700" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="200" y1="40" x2="200" y2="50" stroke="#FF8CE8" stroke-width="2" stroke-linecap="round"/>
  <line x1="195" y1="45" x2="205" y2="45" stroke="#FF8CE8" stroke-width="2" stroke-linecap="round"/>
""")

def s03_six_years():
    h = HEAD(120, 65)
    return WRAP(f"""
{BG("#FFE4E1","#FFF0F5")}
{SHADOW(120,228)}
{h}
  <!-- body pink party outfit -->
  <rect x="87" y="141" width="66" height="52" rx="13" fill="#E91E8C"/>
  <!-- party hat -->
  <polygon points="120,22 95,68 145,68" fill="#FF6B6B"/>
  <polygon points="120,22 95,68 145,68" fill="none" stroke="white" stroke-width="1.5" stroke-dasharray="4,3"/>
  <circle cx="120" cy="22" r="5" fill="#FFD700"/>
  <!-- left arm holds cake -->
  <rect x="54" y="141" width="35" height="14" rx="7" fill="#E91E8C"/>
  <circle cx="51" cy="145" r="11" fill="{SK}"/>
  <!-- right arm up (6 fingers) -->
  <rect x="152" y="120" width="14" height="32" rx="7" fill="#E91E8C"/>
  <circle cx="158" cy="114" r="11" fill="{SK}"/>
  <!-- "6" finger lines on hand -->
  <line x1="152" y1="108" x2="152" y2="102" stroke="{SK}" stroke-width="4" stroke-linecap="round"/>
  <line x1="156" y1="107" x2="156" y2="100" stroke="{SK}" stroke-width="4" stroke-linecap="round"/>
  <line x1="160" y1="108" x2="160" y2="101" stroke="{SK}" stroke-width="4" stroke-linecap="round"/>
  <!-- cake in left hand -->
  <rect x="28" y="145" width="44" height="34" rx="5" fill="#FFFDE7" stroke="#FFD700" stroke-width="1.5"/>
  <rect x="28" y="145" width="44" height="10" rx="5" fill="#FF8CE8"/>
  <!-- 6 candles -->
  <rect x="34" y="130" width="4" height="17" rx="2" fill="#4A90D9"/>
  <rect x="40" y="128" width="4" height="19" rx="2" fill="#FF6B6B"/>
  <rect x="46" y="130" width="4" height="17" rx="2" fill="#69F0AE"/>
  <rect x="52" y="129" width="4" height="18" rx="2" fill="#FFD700"/>
  <rect x="58" y="131" width="4" height="16" rx="2" fill="#FF8CE8"/>
  <rect x="64" y="130" width="4" height="17" rx="2" fill="#FF6B6B"/>
  <!-- flames on candles -->
  <ellipse cx="36" cy="128" rx="3" ry="4" fill="#FFD700"/>
  <ellipse cx="42" cy="126" rx="3" ry="4" fill="#FF8C00"/>
  <ellipse cx="48" cy="128" rx="3" ry="4" fill="#FFD700"/>
  <ellipse cx="54" cy="127" rx="3" ry="4" fill="#FF8C00"/>
  <ellipse cx="60" cy="129" rx="3" ry="4" fill="#FFD700"/>
  <ellipse cx="66" cy="128" rx="3" ry="4" fill="#FF8C00"/>
{LEGS(120,189,"#E91E8C")}
""")

def s04_want_firefighter():
    h = HEAD(120, 80)
    return WRAP(f"""
{BG("#1A1A4E","#2D1B6B")}
{SHADOW(120,228)}
  <!-- stars -->
  <circle cx="30" cy="25" r="2" fill="white" opacity="0.8"/>
  <circle cx="60" cy="15" r="1.5" fill="white" opacity="0.6"/>
  <circle cx="200" cy="20" r="2" fill="white" opacity="0.8"/>
  <circle cx="220" cy="45" r="1.5" fill="white" opacity="0.6"/>
  <circle cx="180" cy="10" r="2" fill="white"/>
  <circle cx="45" cy="50" r="1.5" fill="white" opacity="0.7"/>
  <!-- bed -->
  <rect x="30" y="185" width="180" height="30" rx="10" fill="#8B4513"/>
  <rect x="30" y="175" width="180" height="20" rx="8" fill="#FFFDE7"/>
  <!-- pillow -->
  <ellipse cx="90" cy="176" rx="35" ry="12" fill="white" opacity="0.9"/>
  <!-- blanket over body -->
  <rect x="60" y="178" width="130" height="30" rx="8" fill="#3F51B5" opacity="0.9"/>
{h}
  <!-- sleeping face - eyes closed -->
  <path d="M 107 82 Q 112 78 117 82" stroke="#222" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M 123 82 Q 128 78 133 82" stroke="#222" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- thought bubble -->
  <circle cx="170" cy="120" r="4" fill="white" opacity="0.7"/>
  <circle cx="180" cy="108" r="5" fill="white" opacity="0.8"/>
  <circle cx="192" cy="94" r="7" fill="white" opacity="0.9"/>
  <ellipse cx="195" cy="58" rx="40" ry="30" fill="white" opacity="0.92"/>
  <!-- fire helmet in thought bubble -->
  <path d="M 170 60 Q 170 38 195 36 Q 220 38 220 60 Z" fill="#E53935"/>
  <rect x="163" y="57" width="64" height="10" rx="5" fill="#C62828"/>
  <circle cx="195" cy="50" r="7" fill="#FFD600"/>
  <text x="195" y="55" text-anchor="middle" font-size="9" font-weight="900" fill="#B71C1C" font-family="Arial">1</text>
  <!-- ZZZ -->
  <text x="140" y="55" font-size="16" fill="#FFD700" font-family="Arial" font-weight="900" opacity="0.8">Z</text>
  <text x="152" y="44" font-size="12" fill="#FFD700" font-family="Arial" font-weight="900" opacity="0.7">z</text>
  <text x="161" y="36" font-size="9" fill="#FFD700" font-family="Arial" font-weight="900" opacity="0.6">z</text>
""")

def s05_brave_firefighter():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#FF8C00","#FF5722")}
{SHADOW(120,228)}
  <!-- flames background -->
  <path d="M 20 240 C 10 210 25 195 15 175 C 20 190 30 183 25 162 C 32 178 38 172 33 192 C 40 182 42 196 38 210 Z" fill="#FF6D00" opacity="0.8"/>
  <path d="M 22 240 C 16 215 26 203 20 185 C 24 197 30 192 26 172 Z" fill="#FFD600" opacity="0.6"/>
  <path d="M 210 240 C 200 210 215 195 205 175 C 210 190 220 183 215 162 C 222 178 228 172 223 192 C 230 182 232 196 228 210 Z" fill="#FF6D00" opacity="0.8"/>
  <path d="M 212 240 C 206 215 216 203 210 185 C 214 197 220 192 216 172 Z" fill="#FFD600" opacity="0.6"/>
{h}
  <!-- fire helmet -->
  <path d="M 78 74 Q 78 34 120 32 Q 162 34 162 74 Z" fill="#E53935"/>
  <rect x="72" y="70" width="96" height="12" rx="6" fill="#C62828"/>
  <circle cx="120" cy="54" r="10" fill="#FFD600"/>
  <text x="120" y="59" text-anchor="middle" font-size="10" font-weight="900" fill="#B71C1C" font-family="Arial">1</text>
  <!-- body red uniform -->
  <rect x="87" y="148" width="66" height="52" rx="13" fill="#E53935"/>
  <!-- yellow reflective stripe -->
  <rect x="87" y="172" width="66" height="9" rx="4" fill="#FFD600"/>
  <!-- left arm raised fist -->
  <rect x="54" y="125" width="14" height="32" rx="7" fill="#E53935"/>
  <circle cx="60" cy="120" r="11" fill="{SK}"/>
  <!-- right arm fist -->
  <rect x="173" y="125" width="14" height="32" rx="7" fill="#E53935"/>
  <circle cx="179" cy="120" r="11" fill="{SK}"/>
{LEGS(120,196,"#E53935","#212121")}
  <!-- star sparkles -->
  <polygon points="42,45 44,52 51,52 45.5,56 47.5,63 42,59 36.5,63 38.5,56 33,52 40,52" fill="#FFD600" opacity="0.9"/>
  <polygon points="198,30 199.5,36 206,36 201,39.5 203,46 198,42.5 193,46 195,39.5 190,36 196.5,36" fill="white" opacity="0.8"/>
""")

def s06_help_people():
    h = HEAD(115, 72)
    return WRAP(f"""
{BG("#4CAF50","#81C784")}
{SHADOW(120,228)}
{h}
  <!-- fire helmet small -->
  <path d="M 76 74 Q 76 42 115 40 Q 154 42 154 74 Z" fill="#E53935"/>
  <rect x="70" y="70" width="90" height="10" rx="5" fill="#C62828"/>
  <!-- body firefighter -->
  <rect x="82" y="148" width="66" height="52" rx="13" fill="#E53935"/>
  <rect x="82" y="172" width="66" height="8" rx="4" fill="#FFD600"/>
  <!-- left arm carrying person -->
  <rect x="47" y="148" width="38" height="14" rx="7" fill="#E53935"/>
  <circle cx="43" cy="151" r="11" fill="{SK}"/>
  <!-- right arm extended -->
  <rect x="150" y="148" width="38" height="14" rx="7" fill="#E53935"/>
  <circle cx="192" cy="152" r="11" fill="{SK}"/>
  <!-- small person being carried on left side -->
  <circle cx="32" cy="128" r="18" fill="{SK}"/>
  <ellipse cx="32" cy="112" rx="16" ry="10" fill="{HR}"/>
  <rect x="18" y="142" width="28" height="30" rx="8" fill="#FF8CE8"/>
  <!-- heart above -->
  <path d="M 175 55 C 175 45 160 40 160 52 C 160 40 145 45 145 55 C 145 65 160 75 160 75 C 160 75 175 65 175 55 Z" fill="#FF5252" opacity="0.9"/>
{LEGS(115,196,"#E53935","#212121")}
""")

def s07_save_lives():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#64B5F6","#90CAF9")}
{SHADOW(120,228)}
{h}
  <!-- fire helmet -->
  <path d="M 78 74 Q 78 34 120 32 Q 162 34 162 74 Z" fill="#E53935"/>
  <rect x="72" y="70" width="96" height="12" rx="6" fill="#C62828"/>
  <!-- body firefighter -->
  <rect x="87" y="148" width="66" height="52" rx="13" fill="#E53935"/>
  <rect x="87" y="172" width="66" height="9" rx="4" fill="#FFD600"/>
  <!-- left arm cradling puppy -->
  <rect x="52" y="148" width="38" height="14" rx="7" fill="#E53935"/>
  <circle cx="49" cy="152" r="11" fill="{SK}"/>
  <!-- right arm -->
  <rect x="152" y="148" width="38" height="14" rx="7" fill="#E53935"/>
  <circle cx="193" cy="152" r="11" fill="{SK}"/>
  <!-- puppy on left arm -->
  <ellipse cx="32" cy="140" rx="20" ry="14" fill="#D2691E"/>
  <circle cx="24" cy="128" r="14" fill="#D2691E"/>
  <ellipse cx="17" cy="120" rx="7" ry="9" fill="#8B4513"/>
  <ellipse cx="31" cy="120" rx="7" ry="9" fill="#8B4513"/>
  <circle cx="21" cy="128" r="3" fill="#333"/>
  <circle cx="27" cy="128" r="3" fill="#333"/>
  <ellipse cx="24" cy="132" rx="4" ry="2.5" fill="#FF8A80"/>
{LEGS(120,196,"#E53935","#212121")}
  <!-- big heart -->
  <path d="M 195 72 C 195 60 178 55 178 68 C 178 55 161 60 161 72 C 161 84 178 95 178 95 C 178 95 195 84 195 72 Z" fill="#FF5252"/>
  <!-- small hearts -->
  <text x="30" y="55" font-size="18" font-family="serif">♥</text>
  <text x="200" y="50" font-size="14" font-family="serif" fill="#FF5252">♥</text>
""")

def s08_woo_woo():
    return WRAP(f"""
{BG("#E3F2FD","#BBDEFB")}
  <!-- road -->
  <rect x="0" y="190" width="240" height="50" fill="#555"/>
  <rect x="0" y="190" width="240" height="5" fill="#444"/>
  <!-- road lines -->
  <rect x="20" y="210" width="30" height="5" rx="2" fill="#FFD700"/>
  <rect x="70" y="210" width="30" height="5" rx="2" fill="#FFD700"/>
  <rect x="120" y="210" width="30" height="5" rx="2" fill="#FFD700"/>
  <rect x="170" y="210" width="30" height="5" rx="2" fill="#FFD700"/>
  <!-- truck body -->
  <rect x="20" y="130" width="170" height="65" rx="12" fill="#E53935"/>
  <!-- truck cab (front) -->
  <rect x="20" y="115" width="70" height="50" rx="10" fill="#C62828"/>
  <!-- windshield -->
  <rect x="28" y="120" width="56" height="36" rx="6" fill="#90CAF9" opacity="0.8"/>
  <!-- windows on body -->
  <rect x="105" y="138" width="30" height="24" rx="5" fill="#90CAF9" opacity="0.7"/>
  <rect x="145" y="138" width="30" height="24" rx="5" fill="#90CAF9" opacity="0.7"/>
  <!-- white stripe -->
  <rect x="20" y="168" width="170" height="10" rx="0" fill="white" opacity="0.4"/>
  <!-- wheels -->
  <circle cx="65" cy="196" r="20" fill="#222"/>
  <circle cx="65" cy="196" r="12" fill="#555"/>
  <circle cx="65" cy="196" r="5" fill="#888"/>
  <circle cx="175" cy="196" r="20" fill="#222"/>
  <circle cx="175" cy="196" r="12" fill="#555"/>
  <circle cx="175" cy="196" r="5" fill="#888"/>
  <!-- siren lights on top -->
  <rect x="80" y="110" width="80" height="18" rx="5" fill="#333"/>
  <circle cx="100" cy="119" r="10" fill="#E53935"/>
  <circle cx="100" cy="119" r="7" fill="#FF6B6B"/>
  <circle cx="140" cy="119" r="10" fill="#1565C0"/>
  <circle cx="140" cy="119" r="7" fill="#42A5F5"/>
  <!-- speed lines -->
  <line x1="0" y1="145" x2="22" y2="145" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.6"/>
  <line x1="0" y1="158" x2="18" y2="158" stroke="white" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
  <line x1="0" y1="165" x2="20" y2="165" stroke="white" stroke-width="2" stroke-linecap="round" opacity="0.4"/>
  <!-- siren glow -->
  <circle cx="100" cy="119" r="18" fill="#E53935" opacity="0.2"/>
  <circle cx="140" cy="119" r="18" fill="#1565C0" opacity="0.2"/>
  <!-- hose on side -->
  <path d="M 190 145 Q 215 148 218 162 Q 220 175 210 178" stroke="#FF8C00" stroke-width="5" fill="none" stroke-linecap="round"/>
""")

def s09_police():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#1565C0","#1976D2")}
{SHADOW(120,228)}
{h}
  <!-- police cap -->
  <rect x="84" y="42" width="72" height="14" rx="6" fill="#0D47A1"/>
  <rect x="76" y="52" width="88" height="8" rx="4" fill="#0D47A1"/>
  <!-- cap badge -->
  <polygon points="120,30 123,39 132,39 125,44 128,53 120,48 112,53 115,44 108,39 117,39" fill="#FFD700"/>
  <!-- body navy uniform -->
  <rect x="87" y="148" width="66" height="52" rx="13" fill="#1A237E"/>
  <!-- badge on chest -->
  <polygon points="120,157 122.5,165 130.5,165 124,169 126.5,177 120,173 113.5,177 116,169 109.5,165 117.5,165" fill="#FFD700"/>
  <!-- left arm thumbs up -->
  <rect x="52" y="148" width="38" height="14" rx="7" fill="#1A237E"/>
  <circle cx="48" cy="148" r="11" fill="{SK}"/>
  <!-- thumb up gesture -->
  <rect x="37" y="135" width="10" height="16" rx="5" fill="{SK}"/>
  <!-- right arm -->
  <rect x="152" y="148" width="38" height="14" rx="7" fill="#1A237E"/>
  <circle cx="193" cy="152" r="11" fill="{SK}"/>
{LEGS(120,196,"#1A237E")}
  <!-- stars around -->
  <polygon points="30,50 31.5,56 38,56 32.5,59.5 34.5,66 30,62 25.5,66 27.5,59.5 22,56 28.5,56" fill="#FFD700" opacity="0.8"/>
  <polygon points="210,60 211.5,66 218,66 212.5,69.5 214.5,76 210,72 205.5,76 207.5,69.5 202,66 208.5,66" fill="#FFD700" opacity="0.7"/>
""")

def s10_strong():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#FFF176","#FFFDE7")}
{SHADOW(120,228)}
{h}
  <!-- police cap -->
  <rect x="84" y="42" width="72" height="14" rx="6" fill="#0D47A1"/>
  <rect x="76" y="52" width="88" height="8" rx="4" fill="#0D47A1"/>
  <polygon points="120,30 123,39 132,39 125,44 128,53 120,48 112,53 115,44 108,39 117,39" fill="#FFD700"/>
  <!-- body navy uniform -->
  <rect x="87" y="148" width="66" height="52" rx="13" fill="#1A237E"/>
  <polygon points="120,157 122.5,165 130.5,165 124,169 126.5,177 120,173 113.5,177 116,169 109.5,165 117.5,165" fill="#FFD700"/>
  <!-- left arm FLEXED up -->
  <rect x="48" y="122" width="14" height="36" rx="7" fill="#1A237E"/>
  <!-- bicep bulge left -->
  <ellipse cx="55" cy="119" rx="16" ry="13" fill="#1A237E"/>
  <circle cx="50" cy="115" r="11" fill="{SK}"/>
  <!-- right arm FLEXED up -->
  <rect x="178" y="122" width="14" height="36" rx="7" fill="#1A237E"/>
  <ellipse cx="185" cy="119" rx="16" ry="13" fill="#1A237E"/>
  <circle cx="190" cy="115" r="11" fill="{SK}"/>
{LEGS(120,196,"#1A237E")}
  <!-- power stars -->
  <polygon points="35,85 37,92 44,92 38.5,96 40.5,103 35,99 29.5,103 31.5,96 26,92 33,92" fill="#FF8C00" opacity="0.9"/>
  <polygon points="205,85 207,92 214,92 208.5,96 210.5,103 205,99 199.5,103 201.5,96 196,92 203,92" fill="#FF8C00" opacity="0.9"/>
  <!-- sweat drops (effort) -->
  <path d="M 40 52 Q 38 46 42 42" stroke="#42A5F5" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M 200 52 Q 202 46 198 42" stroke="#42A5F5" stroke-width="2" fill="none" stroke-linecap="round"/>
""")

def s11_catch():
    # Police running after round villain
    h = HEAD(80, 80)
    return WRAP(f"""
{BG("#7E57C2","#9575CD")}
{SHADOW(120,228)}
  <!-- police running LEFT side -->
{h}
  <!-- police cap -->
  <rect x="44" y="50" width="72" height="12" rx="5" fill="#0D47A1"/>
  <rect x="36" y="60" width="88" height="7" rx="3" fill="#0D47A1"/>
  <polygon points="80,38 82.5,47 91.5,47 85,51.5 87.5,59.5 80,55 72.5,59.5 75,51.5 68.5,47 77.5,47" fill="#FFD700"/>
  <!-- body running -->
  <rect x="47" y="156" width="66" height="50" rx="13" fill="#1A237E"/>
  <!-- left arm back -->
  <rect x="20" y="165" width="30" height="13" rx="6" fill="#1A237E"/>
  <circle cx="18" cy="168" r="10" fill="{SK}"/>
  <!-- right arm forward -->
  <rect x="115" y="148" width="30" height="13" rx="6" fill="#1A237E"/>
  <circle cx="148" cy="150" r="10" fill="{SK}"/>
  <!-- legs running pose -->
  <rect x="50" y="200" width="20" height="24" rx="8" fill="#1A237E" transform="rotate(-15 50 200)"/>
  <rect x="78" y="200" width="20" height="24" rx="8" fill="#1A237E" transform="rotate(20 78 200)"/>
  <ellipse cx="58" cy="224" rx="12" ry="5" fill="#333" transform="rotate(-15 58 224)"/>
  <ellipse cx="88" cy="224" rx="12" ry="5" fill="#333" transform="rotate(20 88 224)"/>
  <!-- round villain right side -->
  <circle cx="185" cy="140" r="38" fill="#4CAF50"/>
  <!-- villain face (scared) -->
  <circle cx="174" cy="136" r="7" fill="white"/>
  <circle cx="196" cy="136" r="7" fill="white"/>
  <circle cx="175" cy="137" r="4" fill="#111"/>
  <circle cx="197" cy="137" r="4" fill="#111"/>
  <!-- scared O mouth -->
  <ellipse cx="185" cy="150" rx="8" ry="6" fill="white"/>
  <ellipse cx="185" cy="150" rx="5" ry="4" fill="#222"/>
  <!-- villain hat/mask -->
  <rect x="152" y="105" width="66" height="14" rx="5" fill="#222"/>
  <rect x="162" y="92" width="46" height="20" rx="5" fill="#333"/>
  <!-- handcuffs flying -->
  <circle cx="155" cy="168" r="8" fill="none" stroke="#888" stroke-width="3"/>
  <circle cx="170" cy="170" r="8" fill="none" stroke="#888" stroke-width="3"/>
  <line x1="163" y1="168" x2="162" y2="170" stroke="#888" stroke-width="3"/>
  <!-- speed lines -->
  <line x1="218" y1="135" x2="238" y2="135" stroke="white" stroke-width="2.5" stroke-linecap="round" opacity="0.5"/>
  <line x1="221" y1="148" x2="238" y2="148" stroke="white" stroke-width="2" stroke-linecap="round" opacity="0.4"/>
""")

def s12_keep_safe():
    # Police in front, family behind
    h = HEAD(120, 68)
    return WRAP(f"""
{BG("#FFB300","#FFA000")}
{SHADOW(120,228)}
  <!-- family behind: mom and child small -->
  <!-- mom -->
  <circle cx="172" cy="110" r="28" fill="{SK}"/>
  <ellipse cx="172" cy="88" rx="26" ry="16" fill="#8B4513"/>
  <rect x="154" y="134" width="36" height="40" rx="10" fill="#E91E8C"/>
  <!-- child -->
  <circle cx="64" cy="118" r="22" fill="{SK}"/>
  <ellipse cx="64" cy="100" rx="20" ry="13" fill="{HR}"/>
  <rect x="49" y="136" width="30" height="35" rx="8" fill="#4CAF50"/>
  <!-- police main character -->
{h}
  <!-- shield pose arms wide -->
  <rect x="84" y="42" width="72" height="12" rx="5" fill="#0D47A1"/>
  <rect x="76" y="52" width="88" height="7" rx="3" fill="#0D47A1"/>
  <polygon points="120,30 122.5,38 131.5,38 125,43 127.5,51 120,46 112.5,51 115,43 108.5,38 117.5,38" fill="#FFD700"/>
  <!-- body navy -->
  <rect x="87" y="144" width="66" height="52" rx="13" fill="#1A237E"/>
  <polygon points="120,154 122.5,162 130.5,162 124,167 126.5,174 120,170 113.5,174 116,167 109.5,162 117.5,162" fill="#FFD700"/>
  <!-- arms spread wide as shield -->
  <rect x="30" y="144" width="60" height="14" rx="7" fill="#1A237E"/>
  <circle cx="27" cy="149" r="12" fill="{SK}"/>
  <rect x="152" y="144" width="60" height="14" rx="7" fill="#1A237E"/>
  <circle cx="215" cy="149" r="12" fill="{SK}"/>
{LEGS(120,192,"#1A237E")}
  <!-- shield glow -->
  <ellipse cx="120" cy="165" rx="90" ry="70" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
""")

def s13_doctor_child():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#E0F7FA","#B2EBF2")}
{SHADOW(120,228)}
{h}
  <!-- white doctor coat (oversized) -->
  <rect x="78" y="148" width="84" height="60" rx="14" fill="white" stroke="#B2EBF2" stroke-width="2"/>
  <!-- coat lapels -->
  <path d="M 112 148 L 120 162 L 128 148" fill="#B2EBF2" opacity="0.5"/>
  <!-- pockets -->
  <rect x="85" y="180" width="20" height="15" rx="4" fill="#E0F7FA"/>
  <rect x="135" y="180" width="20" height="15" rx="4" fill="#E0F7FA"/>
  <!-- stethoscope -->
  <path d="M 100 155 Q 90 170 95 185 Q 100 195 115 195 Q 130 195 135 185 Q 140 170 130 155" stroke="#888" stroke-width="3" fill="none"/>
  <circle cx="115" cy="197" r="8" fill="#888"/>
  <circle cx="115" cy="197" r="5" fill="#AAA"/>
  <!-- left arm holds chart -->
  <rect x="44" y="148" width="38" height="14" rx="7" fill="white" stroke="#B2EBF2" stroke-width="2"/>
  <circle cx="41" cy="152" r="11" fill="{SK}"/>
  <!-- clipboard -->
  <rect x="18" y="130" width="30" height="38" rx="4" fill="white" stroke="#90A4AE" stroke-width="1.5"/>
  <rect x="22" y="118" width="22" height="8" rx="3" fill="#90A4AE"/>
  <line x1="22" y1="140" x2="44" y2="140" stroke="#90A4AE" stroke-width="1.5"/>
  <line x1="22" y1="146" x2="44" y2="146" stroke="#90A4AE" stroke-width="1.5"/>
  <line x1="22" y1="152" x2="44" y2="152" stroke="#90A4AE" stroke-width="1.5"/>
  <!-- right arm up excited -->
  <rect x="160" y="130" width="14" height="30" rx="7" fill="white" stroke="#B2EBF2" stroke-width="2"/>
  <circle cx="166" cy="124" r="11" fill="{SK}"/>
{LEGS(120,204,"white","#B0BEC5")}
  <!-- cross on coat -->
  <rect x="117" y="162" width="6" height="18" rx="3" fill="#EF5350" opacity="0.7"/>
  <rect x="111" y="168" width="18" height="6" rx="3" fill="#EF5350" opacity="0.7"/>
""")

def s14_doctors_kind():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#FCE4EC","#F8BBD0")}
{SHADOW(120,228)}
{h}
  <!-- white doctor coat -->
  <rect x="83" y="148" width="74" height="56" rx="14" fill="white" stroke="#F8BBD0" stroke-width="2"/>
  <path d="M 108 148 L 120 160 L 132 148" fill="#F8BBD0" opacity="0.5"/>
  <!-- cross -->
  <rect x="117" y="158" width="6" height="18" rx="3" fill="#EF5350" opacity="0.7"/>
  <rect x="111" y="164" width="18" height="6" rx="3" fill="#EF5350" opacity="0.7"/>
  <!-- arms out gentle -->
  <rect x="47" y="148" width="38" height="14" rx="7" fill="white" stroke="#F8BBD0" stroke-width="2"/>
  <circle cx="44" cy="152" r="11" fill="{SK}"/>
  <rect x="155" y="148" width="38" height="14" rx="7" fill="white" stroke="#F8BBD0" stroke-width="2"/>
  <circle cx="196" cy="152" r="11" fill="{SK}"/>
{LEGS(120,200,"white","#BDBDBD")}
  <!-- BIG HEART -->
  <path d="M 135 44 C 135 28 112 22 112 38 C 112 22 89 28 89 44 C 89 60 112 78 112 78 C 112 78 135 60 135 44 Z" fill="#FF5252"/>
  <!-- small hearts floating -->
  <path d="M 168 90 C 168 85 161 83 161 88 C 161 83 154 85 154 90 C 154 95 161 100 161 100 C 161 100 168 95 168 90 Z" fill="#FF8A80"/>
  <path d="M 88 35 C 88 31 83 30 83 34 C 83 30 78 31 78 35 C 78 39 83 43 83 43 C 83 43 88 39 88 35 Z" fill="#FF8A80"/>
  <path d="M 178 55 C 178 51 173 50 173 54 C 173 50 168 51 168 55 C 168 59 173 63 173 63 C 173 63 178 59 178 55 Z" fill="#FF5252" opacity="0.7"/>
""")

def s15_help_sick():
    # Doctor (left) handing medicine to sniffling patient (right)
    hd = HEAD(75, 78)
    return WRAP(f"""
{BG("#E8F5E9","#C8E6C9")}
{SHADOW(120,228)}
  <!-- doctor -->
{hd}
  <rect x="42" y="154" width="66" height="52" rx="13" fill="white" stroke="#C8E6C9" stroke-width="2"/>
  <rect x="72" y="160" width="6" height="16" rx="3" fill="#EF5350" opacity="0.6"/>
  <rect x="66" y="166" width="18" height="6" rx="3" fill="#EF5350" opacity="0.6"/>
  <!-- doctor right arm handing medicine -->
  <rect x="110" y="154" width="40" height="13" rx="6" fill="white" stroke="#C8E6C9" stroke-width="2"/>
  <circle cx="153" cy="158" r="10" fill="{SK}"/>
  <!-- doctor left arm -->
  <rect x="10" y="154" width="34" height="13" rx="6" fill="white" stroke="#C8E6C9" stroke-width="2"/>
  <circle cx="8" cy="158" r="10" fill="{SK}"/>
{LEGS(75,202,"white","#9E9E9E")}
  <!-- medicine bottle -->
  <rect x="148" y="140" width="20" height="28" rx="5" fill="#FF5252"/>
  <rect x="151" y="133" width="14" height="10" rx="3" fill="#EF5350"/>
  <rect x="150" y="151" width="20" height="5" rx="0" fill="white" opacity="0.3"/>
  <!-- plus sign on bottle -->
  <rect x="156" y="145" width="4" height="12" rx="2" fill="white"/>
  <rect x="152" y="149" width="12" height="4" rx="2" fill="white"/>
  <!-- patient (right side, sitting/sad) -->
  <circle cx="188" cy="115" r="32" fill="{SK}"/>
  <ellipse cx="188" cy="98" rx="28" ry="17" fill="{HR}"/>
  <!-- patient eyes sad -->
  <circle cx="178" cy="112" r="7" fill="white"/>
  <circle cx="198" cy="112" r="7" fill="white"/>
  <circle cx="179" cy="113" r="4" fill="#222"/>
  <circle cx="199" cy="113" r="4" fill="#222"/>
  <!-- sad eyebrows -->
  <path d="M 173 106 Q 178 103 182 107" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M 194 107 Q 198 103 203 106" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
  <!-- sad mouth -->
  <path d="M 182 122 Q 188 118 194 122" stroke="#C1440E" stroke-width="2" fill="none" stroke-linecap="round"/>
  <!-- nose sniffles -->
  <ellipse cx="188" cy="118" rx="4" ry="3" fill="#F08070"/>
  <!-- snot lines -->
  <line x1="186" y1="121" x2="186" y2="127" stroke="#9CCC65" stroke-width="2" stroke-linecap="round"/>
  <line x1="190" y1="121" x2="190" y2="128" stroke="#9CCC65" stroke-width="2" stroke-linecap="round"/>
  <!-- patient body in blanket -->
  <rect x="162" y="145" width="55" height="60" rx="12" fill="#7986CB"/>
  <!-- tissue -->
  <rect x="195" y="130" width="18" height="14" rx="3" fill="white"/>
""")

def s16_feel_better():
    h = HEAD(120, 62)
    return WRAP(f"""
{BG("#FFFDE7","#FFF9C4")}
{SHADOW(120,228)}
{h}
  <!-- happy face - big smile override -->
  <path d="M 106 90 Q 120 106 134 90" stroke="#C1440E" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <path d="M 108 91 Q 120 104 132 91 Q 120 98 108 91 Z" fill="white" opacity="0.8"/>
  <!-- body jumping (tilted) -->
  <rect x="87" y="142" width="66" height="50" rx="13" fill="#7C4DFF" transform="rotate(-5 120 165)"/>
  <!-- arms up both sides celebrating -->
  <rect x="40" y="115" width="14" height="38" rx="7" fill="#7C4DFF" transform="rotate(20 47 134)"/>
  <circle cx="35" cy="110" r="12" fill="{SK}"/>
  <rect x="186" y="115" width="14" height="38" rx="7" fill="#7C4DFF" transform="rotate(-20 193 134)"/>
  <circle cx="205" cy="110" r="12" fill="{SK}"/>
  <!-- legs jumping -->
  <rect x="92" y="188" width="22" height="25" rx="9" fill="#7C4DFF" transform="rotate(-8 103 200)"/>
  <rect x="126" y="188" width="22" height="25" rx="9" fill="#7C4DFF" transform="rotate(8 137 200)"/>
  <ellipse cx="100" cy="215" rx="13" ry="6" fill="#555" transform="rotate(-8 100 215)"/>
  <ellipse cx="140" cy="215" rx="13" ry="6" fill="#555" transform="rotate(8 140 215)"/>
  <!-- sparkles everywhere -->
  <line x1="28" y1="65" x2="28" y2="79" stroke="#FFD700" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="21" y1="72" x2="35" y2="72" stroke="#FFD700" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="205" y1="65" x2="205" y2="77" stroke="#FF8CE8" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="199" y1="71" x2="211" y2="71" stroke="#FF8CE8" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="50" y1="35" x2="50" y2="45" stroke="#69F0AE" stroke-width="2" stroke-linecap="round"/>
  <line x1="45" y1="40" x2="55" y2="40" stroke="#69F0AE" stroke-width="2" stroke-linecap="round"/>
  <line x1="190" y1="35" x2="190" y2="43" stroke="#FF6B6B" stroke-width="2" stroke-linecap="round"/>
  <line x1="186" y1="39" x2="194" y2="39" stroke="#FF6B6B" stroke-width="2" stroke-linecap="round"/>
  <!-- stars -->
  <polygon points="120,18 122,25 129,25 123.5,29 125.5,36 120,32 114.5,36 116.5,29 111,25 118,25" fill="#FFD700"/>
  <circle cx="70" cy="25" r="5" fill="#FF8CE8"/>
  <circle cx="170" cy="22" r="5" fill="#69F0AE"/>
""")

def s17_help_wide():
    h = HEAD(120, 72)
    return WRAP(f"""
{BG("#FF7043","#FF8A65")}
{SHADOW(120,228)}
{h}
  <!-- body warm orange -->
  <rect x="87" y="148" width="66" height="52" rx="13" fill="#E64A19"/>
  <!-- arms WIDE open -->
  <rect x="18" y="148" width="72" height="14" rx="7" fill="#E64A19"/>
  <circle cx="16" cy="153" r="13" fill="{SK}"/>
  <rect x="152" y="148" width="72" height="14" rx="7" fill="#E64A19"/>
  <circle cx="226" cy="153" r="13" fill="{SK}"/>
{LEGS(120,196,"#E64A19")}
  <!-- hearts floating all around -->
  <path d="M 55 88 C 55 80 43 77 43 85 C 43 77 31 80 31 88 C 31 96 43 104 43 104 C 43 104 55 96 55 88 Z" fill="#FF5252" opacity="0.85"/>
  <path d="M 210 88 C 210 80 198 77 198 85 C 198 77 186 80 186 88 C 186 96 198 104 198 104 C 198 104 210 96 210 88 Z" fill="#FF5252" opacity="0.85"/>
  <path d="M 135 42 C 135 36 126 34 126 40 C 126 34 117 36 117 42 C 117 48 126 54 126 54 C 126 54 135 48 135 42 Z" fill="#FFD700" opacity="0.9"/>
  <path d="M 62 50 C 62 46 56 44 56 48 C 56 44 50 46 50 50 C 50 54 56 58 56 58 C 56 58 62 54 62 50 Z" fill="#FF8CE8" opacity="0.8"/>
  <path d="M 192 50 C 192 46 186 44 186 48 C 186 44 180 46 180 50 C 180 54 186 58 186 58 C 186 58 192 54 192 50 Z" fill="#FF8CE8" opacity="0.8"/>
  <!-- warm glow around body -->
  <circle cx="120" cy="165" r="50" fill="rgba(255,255,200,0.12)" stroke="rgba(255,220,0,0.2)" stroke-width="2"/>
""")

def s18_dream():
    h = HEAD(90, 120)
    return WRAP(f"""
{BG("#0D0D2B","#1A1A4E")}
  <!-- stars -->
  <circle cx="20" cy="20" r="2" fill="white"/>
  <circle cx="50" cy="12" r="1.5" fill="white" opacity="0.8"/>
  <circle cx="200" cy="18" r="2" fill="white"/>
  <circle cx="220" cy="35" r="1.5" fill="white" opacity="0.7"/>
  <circle cx="175" cy="10" r="2" fill="white"/>
  <circle cx="40" cy="45" r="1.5" fill="white" opacity="0.6"/>
  <circle cx="130" cy="22" r="1.5" fill="white" opacity="0.8"/>
  <circle cx="155" cy="38" r="1" fill="white" opacity="0.7"/>
  <!-- pillow + bed -->
  <rect x="20" y="192" width="140" height="28" rx="10" fill="#4A235A"/>
  <ellipse cx="68" cy="192" rx="38" ry="12" fill="#6A1B9A" opacity="0.8"/>
  <!-- blanket -->
  <rect x="25" y="195" width="130" height="25" rx="8" fill="#7B1FA2"/>
  <!-- sleeping character -->
{h}
  <!-- eyes closed (sleep) -->
  <path d="M 76 120 Q 82 116 88 120" stroke="#333" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M 92 120 Q 98 116 104 120" stroke="#333" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- small zzzs -->
  <text x="108" y="105" font-size="12" fill="#FFD700" font-family="Arial" font-weight="700" opacity="0.8">Z</text>
  <text x="118" y="94" font-size="9" fill="#FFD700" font-family="Arial" font-weight="700" opacity="0.6">z</text>
  <!-- dream cloud -->
  <circle cx="148" cy="145" r="7" fill="white" opacity="0.7"/>
  <circle cx="158" cy="135" r="9" fill="white" opacity="0.8"/>
  <circle cx="170" cy="126" r="11" fill="white" opacity="0.9"/>
  <ellipse cx="190" cy="90" rx="48" ry="35" fill="white" opacity="0.92"/>
  <!-- fire helmet mini -->
  <path d="M 157 88 Q 157 72 170 70 Q 183 72 183 88 Z" fill="#E53935"/>
  <rect x="153" y="85" width="34" height="7" rx="3" fill="#C62828"/>
  <circle cx="170" cy="80" r="5" fill="#FFD600"/>
  <!-- police badge mini -->
  <polygon points="195,74 197,80 203,80 198,83.5 200,89.5 195,86 190,89.5 192,83.5 187,80 193,80" fill="#FFD700"/>
  <circle cx="195" cy="80" r="3" fill="#1565C0"/>
  <!-- stethoscope mini -->
  <circle cx="220" cy="80" r="9" fill="white" stroke="#888" stroke-width="2"/>
  <circle cx="220" cy="80" r="5" fill="#EEE"/>
  <path d="M 220 71 Q 215 64 210 65 Q 205 66 207 72" stroke="#888" stroke-width="2" fill="none"/>
  <circle cx="207" cy="72" r="3" fill="#888"/>
""")

def s19_thank_you():
    h = HEAD(120, 65)
    return WRAP(f"""
{BG("#FFF8E1","#FFFDE7")}
{SHADOW(120,228)}
{h}
  <!-- bowing - body tilted forward -->
  <rect x="88" y="141" width="64" height="52" rx="13" fill="#4CAF50" transform="rotate(20 120 165)"/>
  <!-- arms together (bow gesture) -->
  <rect x="78" y="155" width="66" height="14" rx="7" fill="#4CAF50" transform="rotate(20 111 162)"/>
  <circle cx="74" cy="162" r="11" fill="{SK}" transform="rotate(20 74 162)"/>
  <circle cx="148" cy="145" r="11" fill="{SK}" transform="rotate(20 148 145)"/>
{LEGS(120,196,"#4CAF50")}
  <!-- flowers around -->
  <!-- flower 1 (left) -->
  <circle cx="38" cy="80" r="10" fill="#FF8CE8"/>
  <circle cx="28" cy="72" r="9" fill="#FF8CE8"/>
  <circle cx="38" cy="62" r="9" fill="#FF8CE8"/>
  <circle cx="48" cy="72" r="9" fill="#FF8CE8"/>
  <circle cx="38" cy="72" r="10" fill="#FFD700"/>
  <!-- flower 2 (right) -->
  <circle cx="202" cy="80" r="10" fill="#69F0AE"/>
  <circle cx="192" cy="72" r="9" fill="#69F0AE"/>
  <circle cx="202" cy="62" r="9" fill="#69F0AE"/>
  <circle cx="212" cy="72" r="9" fill="#69F0AE"/>
  <circle cx="202" cy="72" r="10" fill="#FFD700"/>
  <!-- flower 3 (top left) -->
  <circle cx="65" cy="30" r="8" fill="#FF6B6B"/>
  <circle cx="57" cy="23" r="7" fill="#FF6B6B"/>
  <circle cx="65" cy="16" r="7" fill="#FF6B6B"/>
  <circle cx="73" cy="23" r="7" fill="#FF6B6B"/>
  <circle cx="65" cy="23" r="8" fill="#FFD700"/>
  <!-- flower 4 (top right) -->
  <circle cx="175" cy="30" r="8" fill="#FF8CE8"/>
  <circle cx="167" cy="23" r="7" fill="#FF8CE8"/>
  <circle cx="175" cy="16" r="7" fill="#FF8CE8"/>
  <circle cx="183" cy="23" r="7" fill="#FF8CE8"/>
  <circle cx="175" cy="23" r="8" fill="#FFD700"/>
  <!-- confetti / petals -->
  <rect x="90" y="28" width="7" height="5" rx="2" fill="#FF6B6B" transform="rotate(30 90 28)"/>
  <rect x="145" y="20" width="7" height="5" rx="2" fill="#69F0AE" transform="rotate(-20 145 20)"/>
  <rect x="110" y="35" width="6" height="4" rx="2" fill="#FFD700" transform="rotate(10 110 35)"/>
""")

# ─── Build & save all ──────────────────────────────────────────────────────────

SCENES = {
    "01_hello":          s01_hello,
    "02_my_name":        s02_my_name,
    "03_six_years":      s03_six_years,
    "04_want_firefighter": s04_want_firefighter,
    "05_brave_firefighter": s05_brave_firefighter,
    "06_help_people":    s06_help_people,
    "07_save_lives":     s07_save_lives,
    "08_woo_woo":        s08_woo_woo,
    "09_police":         s09_police,
    "10_strong":         s10_strong,
    "11_catch":          s11_catch,
    "12_keep_safe":      s12_keep_safe,
    "13_doctor_child":   s13_doctor_child,
    "14_doctors_kind":   s14_doctors_kind,
    "15_help_sick":      s15_help_sick,
    "16_feel_better":    s16_feel_better,
    "17_help_wide":      s17_help_wide,
    "18_dream":          s18_dream,
    "19_thank_you":      s19_thank_you,
}

for name, fn in SCENES.items():
    path = f"{OUT}/{name}.svg"
    with open(path, "w", encoding="utf-8") as f:
        f.write(fn())
    print(f"✅  {name}.svg")

print(f"\n완료! {len(SCENES)}개 SVG → {OUT}/")
