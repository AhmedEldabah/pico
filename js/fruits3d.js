/* ============================================================
   fruits3d.js — procedural 3D fruit built with Three.js (r128)
   Drag to rotate (OrbitControls). Auto-rotates when idle.
   Pauses rendering when off-screen. Honours reduced-motion.
   ============================================================ */
(function () {
  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  /* ---- pseudo value-noise for surface texture (deterministic) ---- */
  function noise3(x, y, z) {
    const s = Math.sin(x * 12.9898 + y * 78.233 + z * 37.719) * 43758.5453;
    return s - Math.floor(s);
  }
  function bump(x, y, z, freq, amp) {
    return (Math.sin(x * freq) * Math.cos(y * freq * 1.3) * Math.sin(z * freq * 0.9)) * amp;
  }

  /* ---- strawberry silhouette profile: t 0(bottom point)..1(top) ---- */
  function strawProfile(t) {
    const r = Math.sin(Math.PI * (0.15 + 0.72 * t)) * Math.pow(clamp(t, 0, 1), 0.35);
    return r;
  }

  /* returns surface point for a unit-sphere direction, deformed to a berry */
  function berryPoint(dir, radius) {
    const y = dir.y;
    const t = (y + 1) / 2;
    const ring = Math.sqrt(Math.max(1e-4, 1 - y * y));
    const factor = strawProfile(t) / ring;
    const p = new THREE.Vector3(dir.x * factor, y * 1.18, dir.z * factor);
    // subtle organic bumps
    const n = bump(p.x, p.y, p.z, 6.0, 0.03);
    p.multiplyScalar(radius * (1 + n));
    return p;
  }

  /* ---------- LEAF (used for calyx / citrus) ---------- */
  function makeLeaf(color) {
    const shape = new THREE.Shape();
    shape.moveTo(0, 0);
    shape.bezierCurveTo(0.18, 0.25, 0.16, 0.75, 0, 1);
    shape.bezierCurveTo(-0.16, 0.75, -0.18, 0.25, 0, 0);
    const geo = new THREE.ExtrudeGeometry(shape, { depth: 0.04, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02, bevelSegments: 2, steps: 1 });
    geo.center();
    const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.55, metalness: 0, side: THREE.DoubleSide });
    return new THREE.Mesh(geo, mat);
  }

  /* ---------- STRAWBERRY ---------- */
  function buildStrawberry() {
    const group = new THREE.Group();
    const R = 1.05;

    // body
    const geo = new THREE.SphereGeometry(1, 96, 128);
    const pos = geo.attributes.position;
    const v = new THREE.Vector3();
    for (let i = 0; i < pos.count; i++) {
      v.set(pos.getX(i), pos.getY(i), pos.getZ(i)).normalize();
      const p = berryPoint(v, R);
      pos.setXYZ(i, p.x, p.y, p.z);
    }
    geo.computeVertexNormals();
    const bodyMat = new THREE.MeshStandardMaterial({
      color: 0xe11d36, roughness: 0.32, metalness: 0.05,
      emissive: 0x3a0008, emissiveIntensity: 0.35
    });
    const body = new THREE.Mesh(geo, bodyMat);
    group.add(body);

    // seeds (achenes) via InstancedMesh
    const seedGeo = new THREE.SphereGeometry(1, 6, 5);
    const seedMat = new THREE.MeshStandardMaterial({ color: 0xf7e2a1, roughness: 0.5, emissive: 0x2a2100, emissiveIntensity: 0.15 });
    const N = 150;
    const seeds = new THREE.InstancedMesh(seedGeo, seedMat, N);
    const m = new THREE.Matrix4(), q = new THREE.Quaternion();
    const scl = new THREE.Vector3(0.022, 0.04, 0.014);
    const up = new THREE.Vector3(0, 1, 0);
    const golden = Math.PI * (3 - Math.sqrt(5));
    let k = 0;
    for (let i = 0; i < N * 1.35 && k < N; i++) {
      const yy = 1 - (i / (N * 1.35)) * 2;
      const t = (yy + 1) / 2;
      if (t > 0.9 || t < 0.05) continue; // leave room for calyx & tip
      const rad = Math.sqrt(1 - yy * yy);
      const th = golden * i;
      const dir = new THREE.Vector3(Math.cos(th) * rad, yy, Math.sin(th) * rad);
      const surf = berryPoint(dir, R);
      // outward normal approx
      const nrm = berryPoint(dir, R + 0.01).sub(berryPoint(dir, R - 0.01)).normalize();
      const pos2 = surf.clone().add(nrm.clone().multiplyScalar(-0.006));
      q.setFromUnitVectors(up, nrm);
      m.compose(pos2, q, scl);
      seeds.setMatrixAt(k++, m);
    }
    seeds.count = k;
    seeds.instanceMatrix.needsUpdate = true;
    group.add(seeds);

    // calyx (green leaves) + stem
    const calyx = new THREE.Group();
    const topY = 1.18 * R * 0.98;
    const leafCount = 7;
    for (let i = 0; i < leafCount; i++) {
      const leaf = makeLeaf(0x2f8f3e);
      const a = (i / leafCount) * Math.PI * 2;
      const len = 0.55 + (i % 2) * 0.12;
      leaf.scale.set(0.5, len, 0.5);
      leaf.position.set(Math.cos(a) * 0.22, topY - 0.02, Math.sin(a) * 0.22);
      leaf.rotation.y = -a + Math.PI / 2;
      leaf.rotation.x = -Math.PI / 2 + 0.7; // splay up/out
      leaf.rotation.z = Math.cos(a) * 0.2;
      calyx.add(leaf);
    }
    const stem = new THREE.Mesh(
      new THREE.CylinderGeometry(0.04, 0.055, 0.3, 8),
      new THREE.MeshStandardMaterial({ color: 0x3f7d2e, roughness: 0.7 })
    );
    stem.position.set(0, topY + 0.12, 0);
    calyx.add(stem);
    group.add(calyx);

    group.userData.spinBoost = body; // for easter egg
    return group;
  }

  /* ---------- MANGO ---------- */
  function buildMango() {
    const group = new THREE.Group();
    const geo = new THREE.SphereGeometry(1, 80, 96);
    const pos = geo.attributes.position;
    const colors = [];
    const v = new THREE.Vector3();
    const cA = new THREE.Color(0xd8402a); // blush end
    const cB = new THREE.Color(0xf5952a); // orange mid
    const cC = new THREE.Color(0xf6cf3c); // golden end
    const cG = new THREE.Color(0x8fae2f); // green near stem
    for (let i = 0; i < pos.count; i++) {
      v.set(pos.getX(i), pos.getY(i), pos.getZ(i));
      // ellipsoid + gentle kidney curve
      v.x *= 1.42; v.y *= 0.94; v.z *= 0.82;
      v.y += 0.12 * v.x * v.x * (v.x > 0 ? -0.3 : 0.25); // slight bend
      const nb = bump(v.x, v.y, v.z, 5, 0.012);
      v.multiplyScalar(1 + nb);
      pos.setXYZ(i, v.x, v.y, v.z);
      // colour along long axis
      const tx = clamp((v.x / 1.42 + 1) / 2, 0, 1);
      let col = new THREE.Color().copy(cA).lerp(cB, clamp(tx * 1.6, 0, 1));
      col.lerp(cC, clamp((tx - 0.5) * 2, 0, 1));
      if (tx > 0.86) col.lerp(cG, (tx - 0.86) / 0.14 * 0.6);
      colors.push(col.r, col.g, col.b);
    }
    geo.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
    geo.computeVertexNormals();
    const mat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.4, metalness: 0.05 });
    group.add(new THREE.Mesh(geo, mat));

    // stem nub at the green end
    const stem = new THREE.Mesh(
      new THREE.CylinderGeometry(0.03, 0.05, 0.22, 8),
      new THREE.MeshStandardMaterial({ color: 0x6f7d2b, roughness: 0.7 })
    );
    stem.position.set(1.36, 0.16, 0);
    stem.rotation.z = -0.5;
    group.add(stem);
    group.scale.setScalar(0.82);
    return group;
  }

  /* ---------- ORANGE / CITRUS ---------- */
  function buildOrange() {
    const group = new THREE.Group();
    const geo = new THREE.SphereGeometry(1, 96, 112);
    const pos = geo.attributes.position;
    const v = new THREE.Vector3();
    for (let i = 0; i < pos.count; i++) {
      v.set(pos.getX(i), pos.getY(i), pos.getZ(i));
      const dir = v.clone().normalize();
      // pebbly citrus skin
      const pit = noise3(dir.x * 8, dir.y * 8, dir.z * 8) * 0.02;
      v.y *= 0.94; // slightly oblate
      v.multiplyScalar(1 + pit + bump(v.x, v.y, v.z, 9, 0.01));
      // navel dimple at bottom
      const d = dir.dot(new THREE.Vector3(0, -1, 0));
      if (d > 0.9) v.multiplyScalar(1 - (d - 0.9) * 1.6);
      pos.setXYZ(i, v.x, v.y, v.z);
    }
    geo.computeVertexNormals();
    const mat = new THREE.MeshStandardMaterial({ color: 0xff861a, roughness: 0.72, metalness: 0.02, emissive: 0x431500, emissiveIntensity: 0.18 });
    group.add(new THREE.Mesh(geo, mat));

    // little stem + two leaves on top
    const stem = new THREE.Mesh(
      new THREE.CylinderGeometry(0.03, 0.04, 0.16, 8),
      new THREE.MeshStandardMaterial({ color: 0x5c7d2a, roughness: 0.7 })
    );
    stem.position.set(0, 0.98, 0);
    group.add(stem);
    for (let i = 0; i < 2; i++) {
      const leaf = makeLeaf(0x358a3a);
      leaf.scale.set(0.42, 0.62, 0.42);
      leaf.position.set(i === 0 ? 0.18 : -0.18, 1.02, 0);
      leaf.rotation.z = i === 0 ? -0.9 : 0.9;
      leaf.rotation.x = -Math.PI / 2 + 0.4;
      group.add(leaf);
    }
    group.scale.setScalar(0.98);
    return group;
  }

  const BUILDERS = { strawberry: buildStrawberry, mango: buildMango, orange: buildOrange };

  /* ---------- VIEWER ---------- */
  function makeViewer(canvas, opts = {}) {
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    camera.position.set(0, 0.15, 4.4);

    // lighting — soft, fruity
    scene.add(new THREE.HemisphereLight(0xffffff, 0x30402f, 0.85));
    const key = new THREE.DirectionalLight(0xffffff, 1.15);
    key.position.set(3, 4, 5);
    scene.add(key);
    const rim = new THREE.DirectionalLight(0xa8e05f, 0.5);
    rim.position.set(-4, 1, -3);
    scene.add(rim);
    const fill = new THREE.DirectionalLight(0xffe6c0, 0.35);
    fill.position.set(0, -3, 2);
    scene.add(fill);

    const controls = new THREE.OrbitControls(camera, canvas);
    controls.enableZoom = false;
    controls.enablePan = false;
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.rotateSpeed = 0.95;
    controls.autoRotate = !REDUCED;
    controls.autoRotateSpeed = opts.autoRotateSpeed || 1.6;

    // soft contact shadow under the fruit (radial sprite on a ground plane)
    const shadowTex = (function () {
      const c = document.createElement("canvas"); c.width = c.height = 128;
      const g = c.getContext("2d");
      const grd = g.createRadialGradient(64, 64, 4, 64, 64, 64);
      grd.addColorStop(0, "rgba(20,40,25,0.42)");
      grd.addColorStop(1, "rgba(20,40,25,0)");
      g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
      return new THREE.CanvasTexture(c);
    })();
    const shadow = new THREE.Mesh(
      new THREE.PlaneGeometry(3.4, 3.4),
      new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })
    );
    shadow.rotation.x = -Math.PI / 2;
    shadow.position.y = -1.35;
    scene.add(shadow);

    let current = null;
    let spinKick = 0;
    let floatT = Math.random() * 6.28;

    function setFruit(name) {
      if (current) {
        scene.remove(current);
        current.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) { (Array.isArray(o.material) ? o.material : [o.material]).forEach((mm) => mm.dispose()); } });
      }
      current = (BUILDERS[name] || BUILDERS.strawberry)();
      scene.add(current);
    }
    setFruit(opts.fruit || "strawberry");

    function resize() {
      const w = canvas.clientWidth || canvas.offsetWidth;
      const h = canvas.clientHeight || canvas.offsetHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);
    resize();

    // pause when off-screen
    let visible = true;
    const io = new IntersectionObserver((es) => { visible = es[0].isIntersecting; }, { threshold: 0.01 });
    io.observe(canvas);

    let raf;
    function loop() {
      raf = requestAnimationFrame(loop);
      if (!visible) return;
      if (spinKick > 0) {
        current.rotation.y += spinKick;
        spinKick *= 0.94;
        if (spinKick < 0.002) spinKick = 0;
      }
      if (!REDUCED && current) {
        floatT += 0.012;
        const fy = Math.sin(floatT) * 0.06;
        current.position.y = fy;
        shadow.scale.setScalar(1.15 - fy * 0.9);
        shadow.material.opacity = 0.9 - fy * 1.2;
      }
      controls.update();
      renderer.render(scene, camera);
    }
    loop();

    return {
      setFruit,
      kickSpin() { spinKick = 0.6; },
      getObject() { return current; },
      dispose() { cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); controls.dispose(); renderer.dispose(); }
    };
  }

  window.PICO_FRUITS = { makeViewer };
})();
