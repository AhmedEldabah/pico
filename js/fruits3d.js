/* ============================================================
   fruits3d.js — loads PICO's real 3D models (glTF/GLB) with
   Three.js. Drag to rotate, auto-rotate when idle, gentle float,
   soft contact shadow. Pauses off-screen. Honours reduced-motion.
   ============================================================ */
(function () {
  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const MODELS = {
    strawberry: "assets/models/strawberry.glb",
    mango:      "assets/models/mango.glb",
    orange:     "assets/models/citrus.glb"
  };
  // per-model orientation tweaks (radians) applied after centring
  const ORIENT = {
    strawberry: { rx: 0,    ry: 0, rz: 0 },
    mango:      { rx: 0,    ry: 0, rz: 0 },
    orange:     { rx: 0,    ry: 0, rz: 0 }
  };

  function makeViewer(canvas, opts = {}) {
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.physicallyCorrectLights = true;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    camera.position.set(0, 0.15, 4.6);

    // lighting — soft studio so the photogrammetry colour reads true
    scene.add(new THREE.HemisphereLight(0xffffff, 0x5a4a44, 1.05));
    const key = new THREE.DirectionalLight(0xffffff, 2.2);
    key.position.set(3, 5, 4); scene.add(key);
    const fill = new THREE.DirectionalLight(0xfff2e8, 1.0);
    fill.position.set(-4, 1, 3); scene.add(fill);
    const back = new THREE.DirectionalLight(0xffffff, 1.1);
    back.position.set(0, 3, -4); scene.add(back);

    const controls = new THREE.OrbitControls(camera, canvas);
    controls.enableZoom = false; controls.enablePan = false;
    controls.enableDamping = true; controls.dampingFactor = 0.08;
    controls.rotateSpeed = 0.95;
    controls.autoRotate = !REDUCED;
    controls.autoRotateSpeed = opts.autoRotateSpeed || 1.5;
    controls.target.set(0, 0, 0);

    // soft contact shadow
    const shadowTex = (function () {
      const c = document.createElement("canvas"); c.width = c.height = 128;
      const g = c.getContext("2d");
      const grd = g.createRadialGradient(64, 64, 4, 64, 64, 64);
      grd.addColorStop(0, "rgba(30,15,20,0.5)"); grd.addColorStop(1, "rgba(30,15,20,0)");
      g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
      return new THREE.CanvasTexture(c);
    })();
    const shadow = new THREE.Mesh(
      new THREE.PlaneGeometry(3.6, 3.6),
      new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })
    );
    shadow.rotation.x = -Math.PI / 2; shadow.position.y = -1.35; scene.add(shadow);

    // loading overlay
    const host = canvas.parentElement;
    let host_pos = getComputedStyle(host).position;
    if (host_pos === "static") host.style.position = "relative";
    const loaderEl = document.createElement("div");
    loaderEl.className = "model-loader";
    loaderEl.innerHTML = '<span class="model-loader__ring"></span>';
    host.appendChild(loaderEl);
    const showLoader = (v) => { loaderEl.classList.toggle("is-on", v); };

    const loader = new THREE.GLTFLoader();
    const wraps = {};              // name -> normalized THREE.Group
    let current = null, spinKick = 0, floatT = Math.random() * 6.28, currentName = null;

    function normalize(root, name) {
      const box = new THREE.Box3().setFromObject(root);
      const size = box.getSize(new THREE.Vector3());
      const center = box.getCenter(new THREE.Vector3());
      const s = 2.3 / Math.max(size.x, size.y, size.z);
      root.position.sub(center);
      root.traverse((o) => {
        if (o.isMesh && o.material) {
          const m = o.material;
          if (m.map) m.map.encoding = THREE.sRGBEncoding;
          m.metalness = 0; m.roughness = 1;
          if (m.normalScale) m.normalScale.set(0.7, 0.7);
          m.needsUpdate = true;
        }
      });
      const spin = new THREE.Group(); spin.add(root);      // inner: gets orientation + kick
      const o = ORIENT[name] || { rx: 0, ry: 0, rz: 0 };
      spin.rotation.set(o.rx, o.ry, o.rz);
      const wrap = new THREE.Group(); wrap.add(spin);       // outer: scale + float
      wrap.scale.setScalar(s);
      wrap.userData.spin = spin;
      return wrap;
    }

    function setFruit(name) {
      currentName = name;
      if (wraps[name]) { swapTo(wraps[name]); return; }
      showLoader(true);
      loader.load(MODELS[name] || MODELS.strawberry,
        (gltf) => { const w = normalize(gltf.scene, name); wraps[name] = w; if (currentName === name) swapTo(w); },
        undefined,
        (err) => { showLoader(false); console.warn("model load failed", err); });
    }
    function swapTo(wrap) {
      if (current && current !== wrap) scene.remove(current);
      current = wrap; scene.add(wrap); showLoader(false);
    }
    setFruit(opts.fruit || "strawberry");

    function resize() {
      const w = canvas.clientWidth || canvas.offsetWidth, h = canvas.clientHeight || canvas.offsetHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    }
    const ro = new ResizeObserver(resize); ro.observe(canvas); resize();

    let visible = true;
    const io = new IntersectionObserver((es) => { visible = es[0].isIntersecting; }, { threshold: 0.01 });
    io.observe(canvas);

    let raf;
    function loop() {
      raf = requestAnimationFrame(loop);
      if (!visible) return;
      if (current) {
        const spin = current.userData.spin;
        if (spinKick > 0) { spin.rotation.y += spinKick; spinKick *= 0.94; if (spinKick < 0.002) spinKick = 0; }
        if (!REDUCED) {
          floatT += 0.012;
          const fy = Math.sin(floatT) * 0.06;
          current.position.y = fy;
          shadow.scale.setScalar(1.15 - fy * 0.9);
          shadow.material.opacity = 0.9 - fy * 1.2;
        }
      }
      controls.update();
      renderer.render(scene, camera);
    }
    loop();

    return {
      setFruit,
      kickSpin() { spinKick = 0.6; },
      dispose() { cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); controls.dispose(); renderer.dispose(); loaderEl.remove(); }
    };
  }

  window.PICO_FRUITS = { makeViewer };
})();
