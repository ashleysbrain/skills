# Procedural Audio Engine Patterns

## Core Pattern: Lazy Context + User Gesture
```javascript
_ensureContext() {
  if (this.ctx) return;
  this.ctx = new (window.AudioContext || window.webkitAudioContext)();
  this.masterGain = this.ctx.createGain();
  this.masterGain.connect(this.ctx.destination);
}
// Call on first click/touch:
document.addEventListener('click', () => audioEngine.resume(), { once: true });
document.addEventListener('touchstart', () => audioEngine.resume(), { once: true, passive: true });
```

## Sound Generators (createBufferSource + filters)

### Rain — Bandpass Filtered White Noise
```javascript
const buffer = ctx.createBuffer(1, 2*sampleRate, sampleRate);
const data = buffer.getChannelData(0);
for (let i=0; i<bufferSize; i++) data[i] = Math.random()*2-1;
source = ctx.createBufferSource(); source.buffer = buffer; source.loop = true;
const bandpass = ctx.createBiquadFilter(); bandpass.type='bandpass'; bandpass.frequency.value=3000; bandpass.Q.value=0.5;
const lowpass = ctx.createBiquadFilter(); lowpass.type='lowpass'; lowpass.frequency.value=8000;
source.connect(bandpass).connect(lowpass).connect(gain);
```

### Ocean — LFO-Modulated Lowpass Noise
```javascript
// Same noise buffer, 4*sampleRate for longer loop
const lfo = ctx.createOscillator(); lfo.frequency.value = 0.08; // ~12 sec cycle
const lfoGain = ctx.createGain(); lfoGain.gain.value = 0.5;
const filter = ctx.createBiquadFilter(); filter.type='lowpass'; filter.frequency.value=2000;
lfo.connect(lfoGain).connect(filter.frequency); // LFO modulates cutoff
source.connect(filter).connect(gain);
lfo.start();
```

### White Noise — Pure White Noise
```javascript
// 2*sampleRate buffer, flat spectrum
source.connect(gain);
```

### Pink Noise — 1/f Noise (Voss-McCartney algorithm)
```javascript
let b0=0,b1=0,b2=0,b3=0,b4=0,b5=0,b6=0;
for (let i=0; i<bufferSize; i++) {
  const white = Math.random()*2-1;
  b0 = 0.99886*b0 + white*0.0555179;
  b1 = 0.99332*b1 + white*0.0750759;
  b2 = 0.96900*b2 + white*0.1538520;
  b3 = 0.86650*b3 + white*0.3104856;
  b4 = 0.55000*b4 + white*0.5329522;
  b5 = -0.7616*b5 - white*0.0168980;
  data[i] = (b0+b1+b2+b3+b4+b5+b6 + white*0.5362) * 0.11;
  b6 = white*0.115926;
}
```

### Forest — Sine + Vibrato
```javascript
source = ctx.createOscillator(); source.type='sine'; source.frequency.value=440;
const vibrato = ctx.createOscillator(); vibrato.frequency.value=5;
const vibratoGain = ctx.createGain(); vibratoGain.gain.value=3;
vibrato.connect(vibratoGain).connect(source.frequency);
vibrato.start();
gain.gain.value = 0.02; // Very quiet
source.connect(gain);
```

### Fan — Lowpass Noise (400Hz)
```javascript
// White noise + lowpass at 400Hz, Q=1
const filter = ctx.createBiquadFilter(); filter.type='lowpass'; filter.frequency.value=400; filter.Q.value=1;
source.connect(filter).connect(gain);
```

## Spatial 8D Audio (StereoPanner)
```javascript
const panner = ctx.createStereoPanner();
// Subtle spread: random position between -0.3 and +0.3
panner.pan.value = (Math.random() - 0.5) * 0.6;
gain.connect(panner).connect(masterGain);
```

## Volume Control (no clicks)
```javascript
setVolume(trackId, volume) {
  const track = this.tracks.get(trackId);
  if (track) {
    track.gain.gain.setValueAtTime(volume, this.ctx.currentTime);
  }
}
setMasterVolume(volume) {
  this.masterGain.gain.setValueAtTime(volume, this.ctx.currentTime);
}
```

## Sleep Timer
```javascript
setTimer(minutes) {
  if (this.scheduledStop) clearTimeout(this.scheduledStop);
  if (minutes <= 0) return;
  this.scheduledStop = setTimeout(() => this.stopAll(), minutes * 60 * 1000);
}
```

## Fade Out
```javascript
stop(trackId) {
  const track = this.tracks.get(trackId);
  const now = this.ctx.currentTime;
  track.gain.gain.setValueAtTime(track.gain.gain.value, now);
  track.gain.gain.linearRampToValueAtTime(0, now + 0.5);
  setTimeout(() => { track.source.stop(); this.tracks.delete(trackId); }, 600);
}
```

## State Sync
Always update reactive state after audio changes:
```javascript
_updateTrackState(trackId, playing) { state.set('soundMix.tracks', tracks.map(...)) }
_updateTrackVolume(trackId, volume) { state.set('soundMix.tracks', tracks.map(...)) }
```

## Browser Compatibility
- Chrome/Edge/Safari/Firefox: Full support
- iOS Safari: Requires user gesture for AudioContext
- Android Chrome: Full support
- No polyfills needed for modern browsers