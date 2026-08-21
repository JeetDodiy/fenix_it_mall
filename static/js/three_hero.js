/* Fenix IT Mall – Three.js Hero */
(function () {
  var canvas = document.getElementById('hero-canvas');
  if (!canvas || typeof THREE === 'undefined') return;

  var W = window.innerWidth, H = window.innerHeight;
  var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(W, H);

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(60, W / H, 0.1, 1000);
  camera.position.z = 30;

  var mouse = { x: 0, y: 0 };
  document.addEventListener('mousemove', function (e) {
    mouse.x = (e.clientX / W - 0.5) * 2;
    mouse.y = -(e.clientY / H - 0.5) * 2;
  });

  /* Particles */
  var N = 500;
  var pos = new Float32Array(N * 3);
  var col = new Float32Array(N * 3);
  for (var i = 0; i < N; i++) {
    pos[i*3]   = (Math.random()-.5)*120;
    pos[i*3+1] = (Math.random()-.5)*80;
    pos[i*3+2] = (Math.random()-.5)*80;
    if (Math.random() > .5) { col[i*3]=.02; col[i*3+1]=.71; col[i*3+2]=.83; }
    else                     { col[i*3]=.66; col[i*3+1]=.33; col[i*3+2]=.97; }
  }
  var pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  pGeo.setAttribute('color',    new THREE.BufferAttribute(col, 3));
  var particles = new THREE.Points(pGeo, new THREE.PointsMaterial({ size:.3, vertexColors:true, transparent:true, opacity:.7 }));
  scene.add(particles);

  /* Floating shapes */
  var shapes = [];
  var geos = [new THREE.OctahedronGeometry(1.5,0), new THREE.TetrahedronGeometry(1.8,0),
              new THREE.IcosahedronGeometry(1.3,0), new THREE.BoxGeometry(2,2,2),
              new THREE.OctahedronGeometry(1.2,0),  new THREE.TetrahedronGeometry(1.4,0)];
  var clrs = [0x06b6d4,0xa855f7,0x10b981,0x3b82f6,0xf59e0b,0xec4899];
  geos.forEach(function(g, j) {
    var m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color:clrs[j], wireframe:true, transparent:true, opacity:.3 }));
    m.position.set((Math.random()-.5)*40, (Math.random()-.5)*24, (Math.random()-.5)*20-5);
    m.userData = { rx:(Math.random()-.5)*.014, ry:(Math.random()-.5)*.014, amp:Math.random()*.8+.3, freq:Math.random()*.5+.3, oy:m.position.y };
    scene.add(m); shapes.push(m);
  });

  var clock = new THREE.Clock();
  function tick() {
    requestAnimationFrame(tick);
    var t = clock.getElapsedTime();
    particles.rotation.y = t * .03;
    particles.rotation.x = t * .015;
    camera.position.x += (mouse.x * 3 - camera.position.x) * .04;
    camera.position.y += (mouse.y * 2 - camera.position.y) * .04;
    camera.lookAt(scene.position);
    shapes.forEach(function(s) {
      s.rotation.x += s.userData.rx;
      s.rotation.y += s.userData.ry;
      s.position.y = s.userData.oy + Math.sin(t * s.userData.freq) * s.userData.amp;
    });
    renderer.render(scene, camera);
  }
  tick();

  window.addEventListener('resize', function() {
    W = window.innerWidth; H = window.innerHeight;
    camera.aspect = W/H; camera.updateProjectionMatrix();
    renderer.setSize(W, H);
  });
})();
