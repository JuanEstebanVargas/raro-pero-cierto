import React from 'react';
import {
  AbsoluteFill,
  Audio,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from 'remotion';
import '@fontsource/montserrat/800.css';
import '@fontsource/montserrat/900.css';
import {C, FUENTE} from './marca';

export const FPS = 30;

export type Palabra = {w: string; s: number; e: number};
export type Escena =
  | {tipo: 'svg'; inicio: number; fin: number; svg: string; etiqueta?: string}
  | {tipo: 'numero'; inicio: number; fin: number; valor: number; decimales?: number; unidad?: string; etiqueta: string}
  | {tipo: 'comparacion'; inicio: number; fin: number; a: {nombre: string; valor: number; texto: string}; b: {nombre: string; valor: number; texto: string}}
  | {tipo: 'lista'; inicio: number; fin: number; titulo: string; items: string[]}
  | {tipo: 'cierre'; inicio: number; fin: number};

export type DatoProps = {
  id: string;
  tema: string; // etiqueta corta, p. ej. "CUERPO", "ESPACIO"
  titulo: string; // gancho, 2 a 5 palabras
  tituloAcento: string; // parte resaltada del gancho
  duracion: number; // segundos
  audio: string; // ruta relativa a public/
  musica?: string; // ruta relativa a public/, opcional
  escenas: Escena[];
  palabras: Palabra[];
  fuente: string; // cita corta de la fuente principal
  evidencia: string; // p. ej. "Revisión científica", "Dato histórico", "NASA"
};

const sec = (f: number) => f / FPS;

/* ---------- piezas comunes ---------- */

const Fondo: React.FC = () => {
  const frame = useCurrentFrame();
  const off = (frame * 0.4) % 60;
  return (
    <AbsoluteFill style={{background: C.papel}}>
      <svg width="1080" height="1920" style={{position: 'absolute', opacity: 0.35}}>
        <defs>
          <pattern id="pts" width="60" height="60" patternUnits="userSpaceOnUse" patternTransform={`translate(${off} ${off})`}>
            <circle cx="30" cy="30" r="3" fill={C.papelOscuro} />
          </pattern>
        </defs>
        <rect width="1080" height="1920" fill="url(#pts)" />
      </svg>
    </AbsoluteFill>
  );
};

const Cabecera: React.FC<{tema: string}> = ({tema}) => (
  <div style={{position: 'absolute', top: 70, left: 60, right: 60, display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontFamily: FUENTE}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 14}}>
      <div style={{width: 54, height: 54, borderRadius: 27, background: C.tinta, display: 'flex', alignItems: 'center', justifyContent: 'center', color: C.amarillo, fontWeight: 900, fontSize: 34}}>?</div>
      <div style={{fontWeight: 900, fontSize: 34, color: C.tinta, letterSpacing: 1}}>RARO PERO CIERTO</div>
    </div>
    <div style={{background: C.magenta, color: C.blanco, fontWeight: 900, fontSize: 28, padding: '10px 22px', borderRadius: 12, letterSpacing: 2}}>{tema.toUpperCase()}</div>
  </div>
);

const Titulo: React.FC<{titulo: string; acento: string; grande?: boolean}> = ({titulo, acento, grande}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 12, stiffness: 140}});
  const size = grande ? 120 : 76;
  return (
    <div style={{position: 'absolute', top: grande ? 560 : 190, left: 50, right: 50, textAlign: 'center', fontFamily: FUENTE, fontWeight: 900, lineHeight: 1.02, transform: `scale(${interpolate(s, [0, 1], [0.6, 1])})`, opacity: s}}>
      <div style={{fontSize: size, color: C.tinta}}>{titulo.toUpperCase()}</div>
      <div style={{display: 'inline-block', marginTop: 14, fontSize: size, color: C.tinta, background: C.amarillo, padding: '4px 22px', borderRadius: 16, transform: 'rotate(-2deg)'}}>{acento.toUpperCase()}</div>
    </div>
  );
};

const Subtitulos: React.FC<{palabras: Palabra[]}> = ({palabras}) => {
  const frame = useCurrentFrame();
  const t = sec(frame);
  // grupos de hasta 3 palabras, cortando en signos de puntuación
  const grupos: Palabra[][] = [];
  let g: Palabra[] = [];
  palabras.forEach((p) => {
    g.push(p);
    if (g.length === 3 || /[.,;:?!]$/.test(p.w)) {
      grupos.push(g);
      g = [];
    }
  });
  if (g.length) grupos.push(g);
  const actual = grupos.find((gr) => t >= gr[0].s - 0.05 && t < gr[gr.length - 1].e + 0.15);
  if (!actual) return null;
  const pop = interpolate(t - actual[0].s, [0, 0.12], [0.85, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', top: 1450, left: 40, right: 40, display: 'flex', justifyContent: 'center', fontFamily: FUENTE}}>
      <div style={{background: C.tinta, borderRadius: 22, padding: '18px 30px', transform: `scale(${pop})`, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 18px', maxWidth: 1000}}>
        {actual.map((p, i) => {
          const activa = t >= p.s && t < p.e + 0.05;
          return (
            <span key={i} style={{fontWeight: 900, fontSize: 70, color: activa ? C.amarillo : C.blanco, textTransform: 'uppercase'}}>
              {p.w.replace(/[.,;:]$/, '')}
            </span>
          );
        })}
      </div>
    </div>
  );
};

const Progreso: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return (
    <div style={{position: 'absolute', bottom: 0, left: 0, height: 14, width: `${(frame / durationInFrames) * 100}%`, background: C.magenta}} />
  );
};

/* ---------- escenas ---------- */

const Entrada: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 11, stiffness: 120}});
  const flota = Math.sin(frame / 18) * 10;
  return (
    <div style={{position: 'absolute', top: 420, left: 0, right: 0, height: 980, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `translateY(${flota}px) scale(${interpolate(s, [0, 1], [0.4, 1])})`, opacity: s}}>
      {children}
    </div>
  );
};

const EscenaSvg: React.FC<{svg: string; etiqueta?: string}> = ({svg, etiqueta}) => (
  <Entrada>
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 24}}>
      {etiqueta ? (
        <div style={{fontFamily: FUENTE, fontWeight: 900, fontSize: 64, color: C.tinta, textAlign: 'center', maxWidth: 960}}>{etiqueta.toUpperCase()}</div>
      ) : null}
      <div style={{width: 820, height: 820}} dangerouslySetInnerHTML={{__html: svg.replace('<svg', '<svg width="820" height="820"')}} />
    </div>
  </Entrada>
);

const EscenaNumero: React.FC<{valor: number; decimales?: number; unidad?: string; etiqueta: string}> = ({valor, decimales = 0, unidad, etiqueta}) => {
  const frame = useCurrentFrame();
  const v = interpolate(frame, [0, 30], [0, valor], {extrapolateRight: 'clamp', easing: (x) => 1 - Math.pow(1 - x, 3)});
  return (
    <Entrada>
      <div style={{textAlign: 'center', fontFamily: FUENTE}}>
        <div style={{fontWeight: 900, fontSize: 260, color: C.magenta, lineHeight: 1}}>
          {v.toLocaleString('es', {minimumFractionDigits: decimales, maximumFractionDigits: decimales})}
          {unidad ? <span style={{fontSize: 110, color: C.tinta}}> {unidad}</span> : null}
        </div>
        <div style={{marginTop: 30, fontWeight: 900, fontSize: 64, color: C.tinta, maxWidth: 940}}>{etiqueta.toUpperCase()}</div>
      </div>
    </Entrada>
  );
};

const EscenaComparacion: React.FC<{a: {nombre: string; valor: number; texto: string}; b: {nombre: string; valor: number; texto: string}}> = ({a, b}) => {
  const frame = useCurrentFrame();
  const max = Math.max(a.valor, b.valor) || 1;
  const crece = interpolate(frame, [8, 38], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const barra = (x: typeof a, color: string) => (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width: 400}}>
      <div style={{fontFamily: FUENTE, fontWeight: 900, fontSize: 56, color: C.tinta, marginBottom: 16}}>{x.texto}</div>
      <div style={{height: 600, display: 'flex', alignItems: 'flex-end'}}>
        <div style={{width: 240, height: 600 * (x.valor / max) * crece, background: color, borderRadius: '24px 24px 0 0', border: `6px solid ${C.tinta}`}} />
      </div>
      <div style={{fontFamily: FUENTE, fontWeight: 900, fontSize: 50, color: C.tinta, marginTop: 18, textAlign: 'center'}}>{x.nombre.toUpperCase()}</div>
    </div>
  );
  return (
    <Entrada>
      <div style={{display: 'flex', gap: 40, alignItems: 'flex-end'}}>
        {barra(a, C.turquesa)}
        {barra(b, C.magenta)}
      </div>
    </Entrada>
  );
};

const EscenaLista: React.FC<{titulo: string; items: string[]}> = ({titulo, items}) => {
  const frame = useCurrentFrame();
  return (
    <Entrada>
      <div style={{fontFamily: FUENTE, width: 920}}>
        <div style={{fontWeight: 900, fontSize: 66, color: C.tinta, marginBottom: 30}}>{titulo.toUpperCase()}</div>
        {items.map((it, i) => {
          const o = interpolate(frame, [i * 12, i * 12 + 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <div key={i} style={{opacity: o, transform: `translateX(${(1 - o) * -60}px)`, display: 'flex', alignItems: 'center', gap: 24, marginBottom: 24}}>
              <div style={{width: 76, height: 76, borderRadius: 38, background: C.amarillo, border: `5px solid ${C.tinta}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 900, fontSize: 40, color: C.tinta}}>{i + 1}</div>
              <div style={{fontWeight: 800, fontSize: 54, color: C.tinta}}>{it}</div>
            </div>
          );
        })}
      </div>
    </Entrada>
  );
};

const EscenaCierre: React.FC<{fuente: string; evidencia: string}> = ({fuente, evidencia}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const golpe = spring({frame, fps, config: {damping: 8, stiffness: 200}});
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', fontFamily: FUENTE}}>
      <div style={{transform: `rotate(-8deg) scale(${interpolate(golpe, [0, 1], [2.4, 1])})`, opacity: golpe, border: `14px solid ${C.magenta}`, borderRadius: 30, padding: '30px 50px', color: C.magenta, fontWeight: 900, fontSize: 120, textAlign: 'center', lineHeight: 1}}>
        RARO<br />PERO<br />CIERTO
      </div>
      <div style={{marginTop: 70, background: C.tinta, color: C.blanco, borderRadius: 18, padding: '16px 28px', fontWeight: 800, fontSize: 34, maxWidth: 940, textAlign: 'center'}}>
        {evidencia.toUpperCase()} · {fuente}
      </div>
      <div style={{marginTop: 40, fontWeight: 900, fontSize: 46, color: C.tinta}}>UN DATO RARO CADA DÍA</div>
    </AbsoluteFill>
  );
};

const RenderEscena: React.FC<{e: Escena; p: DatoProps}> = ({e, p}) => {
  switch (e.tipo) {
    case 'svg':
      return <EscenaSvg svg={e.svg} etiqueta={e.etiqueta} />;
    case 'numero':
      return <EscenaNumero valor={e.valor} decimales={e.decimales} unidad={e.unidad} etiqueta={e.etiqueta} />;
    case 'comparacion':
      return <EscenaComparacion a={e.a} b={e.b} />;
    case 'lista':
      return <EscenaLista titulo={e.titulo} items={e.items} />;
    case 'cierre':
      return <EscenaCierre fuente={p.fuente} evidencia={p.evidencia} />;
  }
};

/* ---------- composiciones ---------- */

export const Dato: React.FC<DatoProps> = (p) => {
  const frame = useCurrentFrame();
  const t = sec(frame);
  const enCierre = p.escenas.some((e) => e.tipo === 'cierre' && t >= e.inicio);
  return (
    <AbsoluteFill>
      <Fondo />
      <Cabecera tema={p.tema} />
      {!enCierre ? <Titulo titulo={p.titulo} acento={p.tituloAcento} /> : null}
      {p.escenas.map((e, i) => (
        <Sequence key={i} from={Math.round(e.inicio * FPS)} durationInFrames={Math.max(1, Math.round((e.fin - e.inicio) * FPS))}>
          <RenderEscena e={e} p={p} />
        </Sequence>
      ))}
      {!enCierre ? <Subtitulos palabras={p.palabras} /> : null}
      <Progreso />
      <Audio src={staticFile(p.audio)} />
      {p.musica ? <Audio src={staticFile(p.musica)} volume={0.08} /> : null}
    </AbsoluteFill>
  );
};

export const Portada: React.FC<DatoProps> = (p) => (
  <AbsoluteFill>
    <Fondo />
    <Cabecera tema={p.tema} />
    <Titulo titulo={p.titulo} acento={p.tituloAcento} grande />
  </AbsoluteFill>
);

export const ejemplo: DatoProps = {
  id: 'ejemplo',
  tema: 'Cuerpo',
  titulo: 'Tu estómago',
  tituloAcento: 'no se digiere',
  duracion: 5,
  audio: 'actual/voz.wav',
  escenas: [{tipo: 'numero', inicio: 0, fin: 5, valor: 1.5, decimales: 1, unidad: 'pH', etiqueta: 'acidez de tu estómago'}],
  palabras: [],
  fuente: 'Ejemplo',
  evidencia: 'Ejemplo',
};
