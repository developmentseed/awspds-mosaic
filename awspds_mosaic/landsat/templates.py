"""awspds_mosaic.templates: HTML and XML templates."""


def landsatlive(endpoint: str, token: str = "") -> str:
    """Landsatlive LIVE."""
    return f"""<!DOCTYPE html>
    <html>
      <head>
        <meta charset='utf-8' />
        <title></title>
        <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />

        <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.js'></script>
        <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.css' rel='stylesheet' />

        <link href="https://api.mapbox.com/mapbox-assembly/v0.23.2/assembly.min.css" rel="stylesheet">
        <script src="https://api.mapbox.com/mapbox-assembly/v0.23.2/assembly.js"></script>

        <script src='https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.js'></script>
        <script src='https://cdn.remotepixel.ca/tile-cover/tilecover.js'></script>
        <script src='https://npmcdn.com/@turf/turf/turf.min.js'></script>

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
        <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>

        <style>
            body {{ margin:0; padding:0; }}
            #map {{ position:absolute; top:0; bottom:0; width:100%; }}
            body {{
                overflow: hidden;
            }}
            body * {{
              -webkit-touch-callout: none;
                -webkit-user-select: none;
                    -moz-user-select: none;
                    -ms-user-select: none;
                        user-select: none;
            }}
            .map {{
                position: absolute;
                top: 0;
                bottom: 0;
                width: 100%;
            }}
            .zoom-info {{
                z-index: 10;
                position: absolute;
                bottom: 17px;
                right: 0;
                padding: 5px;
                width: auto;
                height: auto;
                font-size: 12px;
                color: #000;
            }}
            .loading-map {{
              position: absolute;
              width: 100px;
              height: 100px;
              text-align: center;
              opacity: 1;
              font-size: 60px;
              left: 0;
              bottom: 0;
            }}
            .loading-map.off{{
                opacity: 0;
                -o-transition: all .5s ease;
                -webkit-transition: all .5s ease;
                -moz-transition: all .5s ease;
                -ms-transition: all .5s ease;
                transition: all ease .5s;
                visibility:hidden;
            }}
            .middle-center {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }}

            .middle-center * {{
                display: block;
                padding: 5px;
            }}
            #menu {{
              left: 0;
              top: 0;
              position: absolute;
              z-index: 10;
              background-color: #FFF;
            }}
            #rgb-buttons select {{
              border-radius: 50%;
              line-height: 20px;
              padding: 5px;
              text-align: center;
              text-indent: 6px;
              height: 40px;
              width: 40px;
            }}
        </style>
      </head>
      <body>
        <div id='map' class='map'>
          <div id='loader' class="loading-map z3 color-dark">
            <div class="middle-center">
              <div class="round animation-spin animation--infinite animation--speed-1">
                <svg class='icon icon--l inline-block'><use xlink:href='#icon-satellite'/></svg>
              </div>
            </div>
          </div>
          <div id='zoom' class="zoom-info"><span></span></div>
        </div>
        <div id='menu' class="wmax300">
          <section id='rgb' class="px12 py12 active">
            <div class='txt-m mt6 mb6 color-black'>Band combination</div>
            <div class='select-container wmax-full'>
              <select id='rgb-selection' class='select select--s select--stroke  wmax-full color-black'>
                <option value='4,3,2'>Natural Color (4,3,2)</option>
                <option value='7,6,4'>False Color Urban (7,6,4)</option>
                <option value='5,4,3'>Color Infrared Vegetation (5,4,3)</option>
                <option value='6,5,2'>Agriculture (6,5,2)</option>
                <option value='7,6,5'>Atmospheric Penetration (7,6,5)</option>
                <option value='5,6,2'>Healthy Vegetation (5,6,2)</option>
                <option value='7,5,2'>Forest Burn (7,5,2)</option>
                <option value='5,6,4'>Land/Water (5,6,4)</option>
                <option value='7,5,3'>Natural With Atmo Removal (7,5,3)</option>
                <option value='7,5,4'>Shortwave Infrared (7,5,4)</option>
                <option value='5,7,1'>False color 2 (5,7,1)</option>
                <option value='6,5,4'>Vegetation Analysis (6,5,4)</option>
                <option value='custom'>Custom</option>
              </select>
              <div class='select-arrow color-black'></div>
            </div>
            <div id='rgb-buttons' class='align-center px6 py6'>
              <div class='select-container'>
                <select id='r' disabled class='select select--stroke select--stroke--2 color-red mx6 my6'>
                  <option value="1">01</option>
                  <option value="2">02</option>
                  <option value="3">03</option>
                  <option value="4" selected="selected">04</option>
                  <option value="5">05</option>
                  <option value="6">06</option>
                  <option value="7">07</option>
                  <option value="9">09</option>
                  <option value="10">10</option>
                  <option value="11">11</option>
                </select>
              </div>
              <div class='select-container'>
                <select id='g' disabled class='select select--stroke select--stroke--2 color-green mx6 my6'>
                  <option value="1">01</option>
                  <option value="2">02</option>
                  <option value="3" selected="selected">03</option>
                  <option value="4">04</option>
                  <option value="5">05</option>
                  <option value="6">06</option>
                  <option value="7">07</option>
                  <option value="9">09</option>
                  <option value="10">10</option>
                  <option value="11">11</option>
                </select>
              </div>
              <div class='select-container'>
                <select id='b' disabled class='select select--stroke select--stroke--2 color-blue mx6 my6'>
                  <option value="1">01</option>
                  <option value="2" selected="selected">02</option>
                  <option value="3">03</option>
                  <option value="4">04</option>
                  <option value="5">05</option>
                  <option value="6">06</option>
                  <option value="7">07</option>
                  <option value="9">09</option>
                  <option value="10">10</option>
                  <option value="11">11</option>
                </select>
              </div>
            </div>
          </section>

          <section id='dates' class="px12 py12 active">
            <div class='txt-m mt6 mb6 color-black'>Dates</div>
            <input id='date' class='txt-s'></input>
          </section>

          <section id='cloud' class="px12 py12 active">
            <div class='txt-m mt6 mb6 color-black'>Max Cloud cover: <span id='max-cloud-txt'>75</span>%</div>
            <div class='range'>
              <input id='cloud-cover' type='range' min='0' max='100' step='1' value='75'/>
            </div>
          </section>


          <section id='info' class="px12 py12 active">
            <div class='txt-m mt6 mb6 color-black'>FAQ</div>
            <p><b>Why is this slow?</b>
            Landsat 8 hosted on AWS using external overview which required more GET requests than proper COG.
            Also the geometry stored in STAC metadata is the bbox of each scene, resulting on non-optimized mosaic-json.
            </p>
            <p><b>What are the black/white borders?</b>
            Landsat 8 hosted on AWS doesn't use internal nodata and then it resulted in artefacts when creating the overviews.
            </p>

            <p>Link: <a href="https://github.com/developmentseed/awspds-mosaic" target="_blank">awspds-mosaic</a> Github repo.</p>
          </section>

        </div>
        <script>
        const start = moment().subtract(62, 'days').format('YYYY-MM-DD')
        let calendar = flatpickr('#date', {{
          mode: 'range',
          maxDate: 'today',
          dateFormat: 'Y-m-d',
          defaultDate: [start, "today"]
        }})

        mapboxgl.accessToken = '{token}'
        let style
        if (mapboxgl.accessToken !== '') {{
          style = 'mapbox://styles/mapbox/basic-v9'
        }} else {{
          style = {{ version: 8, sources: {{}}, layers: [] }}
        }}

        const overTileZoom = 5

        const scope = {{geom: undefined, mosaicid: undefined, start: "", end: ""}}

        var map = new mapboxgl.Map({{
          container: 'map',
          style: style,
          center: [ -80.123086, 25.992706 ],
          attributionControl: true,
          minZoom: 8,
          maxZoom: 12,
          zoom: 8,
          hash: true
        }})

        map.addControl(new mapboxgl.NavigationControl())

        const updateLayer = () => {{
          if (map.getLayer('raster')) map.removeLayer('raster')
          if (map.getSource('raster')) map.removeSource('raster')
          if (!scope.mosaicid) return

          document.getElementById('loader').classList.toggle('off')
          const r = document.getElementById('r').value
          const g = document.getElementById('g').value
          const b = document.getElementById('b').value
          const params = {{
            pixel_selection: 'first',
            bands: [r, g, b].join(','),
            color_ops: 'gamma RGB 3.5, saturation 1.7, sigmoidal RGB 15 0.35',
            tile_format: 'jpg'
          }}

          const url = new URL(`{endpoint}/tiles/${{scope.mosaicid}}/tilejson.json`)
          Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

          map.addSource('raster', {{ type: 'raster', url: url.href }})
          map.addLayer({{ id: 'raster', type: 'raster', source: 'raster' }})

          document.getElementById('loader').classList.toggle('off')
        }}

        const updateRasterTile = (geom) => {{
          document.getElementById('loader').classList.toggle('off')
          const viewPortTilesGeoJSON = cover.geojson(geom.geometry, {{
            min_zoom: overTileZoom,
            max_zoom: overTileZoom
          }})
          const overTileBbox = turf.bbox(viewPortTilesGeoJSON)
          const overTileGeoJSON = turf.bboxPolygon(overTileBbox)
          scope.geom = overTileGeoJSON

          const r = document.getElementById('r').value
          const g = document.getElementById('g').value
          const b = document.getElementById('b').value
          const params = {{
            pixel_selection: 'first',
            bands: [r, g, b].join(','),
            color_ops: 'gamma RGB 3.5, saturation 1.7, sigmoidal RGB 15 0.35',
            minzoom: 8,
            maxzoom: 12,
            maximum_items_per_tile: 0,
            optimized_selection: true,
            tile_format: 'jpg'
          }}

          const url = new URL('{endpoint}/mosaic/create')
          Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

          const min_cloud = 0
          const max_cloud = parseFloat(document.getElementById('cloud-cover').value)

          scope.start = moment(calendar.selectedDates[0]).format('YYYY-MM-DDTmm:HH:ss')
          scope.end = moment(calendar.selectedDates[1]).format('YYYY-MM-DDTmm:HH:ss')

          const body = {{
            "bbox": overTileBbox,
            "time": `${{scope.start}}Z/${{scope.end}}Z`,
            "query": {{
              "eo:cloud_cover": {{"gte": min_cloud, "lt": max_cloud}},
              "eo:sun_elevation": {{"gt": 0}},
              "landsat:tier": {{"eq": "T1"}},
              "collection": {{"eq": "landsat-8-l1"}},
            }},
            "limit": 1000
          }}

          fetch(url, {{ mode: 'cors', method: "POST", body: JSON.stringify(body) }})
            .then(res => {{
              if (res.ok) return res.json()
              throw new Error('Network response was not ok.')
            }})
            .then(tilejson => {{
              if (map.getLayer('raster')) map.removeLayer('raster')
              if (map.getSource('raster')) map.removeSource('raster')
              scope.mosaicid = tilejson.name
              map.addSource('raster', {{
                type: 'raster',
                tiles: tilejson.tiles,
                tileSize: 256,
                bounds: tilejson.bounds,
                minzoom: tilejson.minzoom,
                maxzoom: tilejson.maxzoom,
              }})
              map.addLayer({{ id: 'raster', type: 'raster', source: 'raster' }})
            }})
            .catch(err => {{
              scope.geom = undefined
              scope.mosaicid = undefined
              console.warn(err)
            }})
            .then(() => {{
              document.getElementById('loader').classList.toggle('off')
            }})
        }}

        // LOAD
        map.on('load', () => {{
          document.getElementById('loader').classList.toggle('off')
          const latLngBounds = map.getBounds()
          const viewportBbox = [
            latLngBounds.getWest(), latLngBounds.getSouth(), latLngBounds.getEast(), latLngBounds.getNorth()
          ]
          const viewPortGeoJSON = turf.bboxPolygon(viewportBbox)
          updateRasterTile(viewPortGeoJSON)
        }})

        // ZOOM
        map.on('zoom', function (e) {{
          const z = (map.getZoom()).toString().slice(0, 6)
          document.getElementById('zoom').textContent = z
        }})

        // MOVE
        map.on('moveend', function (e) {{
          if (map.getZoom() < 7) throw new Error('please zoom')
          const latLngBounds = map.getBounds()
          const viewportBbox = [
            latLngBounds.getWest(), latLngBounds.getSouth(), latLngBounds.getEast(), latLngBounds.getNorth()
          ]
          const viewPortGeoJSON = turf.bboxPolygon(viewportBbox)

          if (scope.mosaicid) {{
            if (!turf.booleanContains(scope.geom, viewPortGeoJSON)) updateRasterTile(viewPortGeoJSON)
          }} else {{
            updateRasterTile(viewPortGeoJSON)
          }}
        }})

        document.getElementById('rgb-selection').addEventListener('change', (e) => {{
          let rgb = e.target.value
          if (rgb === 'custom') {{
            document.getElementById('rgb-buttons').querySelectorAll('select').forEach(function(e){{
              e.disabled = false
            }})
          }} else {{
            document.getElementById('rgb-buttons').querySelectorAll('select').forEach(function(e){{
              e.disabled = true
            }})
            rgb = rgb.split(',')
            document.getElementById('r').value = rgb[0]
            document.getElementById('g').value = rgb[1]
            document.getElementById('b').value = rgb[2]
            updateLayer()
          }}
        }})

        document.getElementById('r').addEventListener('change', () => {{
          if (document.getElementById('rgb-selection').value !== 'custom') return;
          updateLayer()
        }})

        document.getElementById('g').addEventListener('change', () => {{
          if (document.getElementById('rgb-selection').value !== 'custom') return;
          updateLayer()
        }})

        document.getElementById('b').addEventListener('change', () => {{
          if (document.getElementById('rgb-selection').value !== 'custom') return;
          updateLayer()
        }})

        document.getElementById('cloud-cover').addEventListener('input', () => {{
          const value = document.getElementById('cloud-cover').value
          document.getElementById('max-cloud-txt').textContent = value
        }});

        document.getElementById('cloud-cover').addEventListener('change', () => {{
          if (map.getZoom() < 7) throw new Error('please zoom')
          const latLngBounds = map.getBounds()
          const viewportBbox = [
            latLngBounds.getWest(), latLngBounds.getSouth(), latLngBounds.getEast(), latLngBounds.getNorth()
          ]
          const viewPortGeoJSON = turf.bboxPolygon(viewportBbox)
          updateRasterTile(viewPortGeoJSON)
        }});

        calendar.config.onChange.push((selectedDates, dateStr, instance) => {{
          if (map.getZoom() < 7) throw new Error('please zoom')
          if (selectedDates.length === 2) {{
            const latLngBounds = map.getBounds()
            const viewportBbox = [
              latLngBounds.getWest(), latLngBounds.getSouth(), latLngBounds.getEast(), latLngBounds.getNorth()
            ]
            const viewPortGeoJSON = turf.bboxPolygon(viewportBbox)

            const start = moment(calendar.selectedDates[0]).format('YYYY-MM-DDTmm:HH:ss')
            const end = moment(calendar.selectedDates[1]).format('YYYY-MM-DDTmm:HH:ss')
            if ((start === scope.start) && (end === scope.end)) {{
              console.log("No date update")
            }}  else {{
              updateRasterTile(viewPortGeoJSON)
            }}
          }}
        }})

      </script>
      </body>
    </html>"""


def timeserie(endpoint: str, token: str) -> str:
    """Landsatlive LIVE."""
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8' />
    <title></title>
    <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />

    <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.js'></script>
    <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.css' rel='stylesheet' />

    <link href="https://api.mapbox.com/mapbox-assembly/v0.23.2/assembly.min.css" rel="stylesheet">
    <script src="https://api.mapbox.com/mapbox-assembly/v0.23.2/assembly.js"></script>

    <script src='https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.js'></script>
    <script src='https://npmcdn.com/@turf/turf/turf.min.js'></script>

    <style>
        body {{ margin:0; padding:0; }}
        #map {{ position:absolute; top:0; bottom:0; width:100%; }}
          body {{
              overflow: hidden;
          }}
          body * {{
             -webkit-touch-callout: none;
               -webkit-user-select: none;
                  -moz-user-select: none;
                   -ms-user-select: none;
                       user-select: none;
          }}
          .loading-map {{
              position: absolute;
              width: 100%;
              height: 100%;
              color: #FFF;
              background-color: #000;
              text-align: center;
              opacity: 0.5;
              font-size: 45px;
          }}
          .loading-map.off{{
              opacity: 0;
              -o-transition: all .5s ease;
              -webkit-transition: all .5s ease;
              -moz-transition: all .5s ease;
              -ms-transition: all .5s ease;
              transition: all ease .5s;
              visibility:hidden;
          }}
          .middle-center {{
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
          }}

          .middle-center * {{
              display: block;
              padding: 5px;
          }}
    </style>
  </head>
  <body>
    <div id='map' class='map'>
      <div id='loader' class="loading-map z3">
        <div class="middle-center">
          <div class="round animation-spin animation--infinite animation--speed-1">
            <svg class='icon icon--l inline-block'><use xlink:href='#icon-satellite'/></svg>
          </div>
        </div>
      </div>

      <div id='ratio-selector' class='toggle-group bg-gray-faint mt12 ml12 absolute left top z2' style="line-height:0">
        <label class='toggle-container'>
          <input value="(b5-b4)/(b5+b4)" checked="checked" name='toggle-ratio' type='radio' />
          <div title='ndvi' class='toggle color-gray-dark-on-hover'>NDVI</div>
        </label>
        <label class='toggle-container'>
          <input value="(b3-b5)/(b3+b5)" name='toggle-ratio' type='radio' />
          <div title='NDWI' class='toggle color-gray-dark-on-hover'>NDWI</div>
        </label>
        <label class='toggle-container'>
          <input value="(b5-b6)/(b5+b6)" name='toggle-ratio' type='radio' />
          <div title='NBR' class='toggle color-gray-dark-on-hover'>NBR</div>
        </label>
      </div>

    </div>
    <script>
mapboxgl.accessToken = '{token}'

var scope = {{ mosaicid: undefined }}

var map = new mapboxgl.Map({{
  container: 'map',
  style: 'mapbox://styles/mapbox/basic-v9',
  center: [ -80.123086, 25.992706 ],
  attributionControl: true,
  minZoom: 2,
  maxZoom: 12,
  zoom: 8,
  hash: true
}})

map.addControl(new mapboxgl.NavigationControl())

map.on('load', () => {{
  document.getElementById('loader').classList.toggle('off')
  map.addSource('landsat', {{
    'type': 'vector',
    'url': 'mapbox://vincentsarago.8ib6ynrs'
  }})

  map.addLayer({{
    'id': 'Grid',
    'type': 'fill',
    'source': 'landsat',
    'source-layer': 'Landsat8_Desc_filtr2',
    'paint': {{
      'fill-color': 'hsla(0, 0%, 0%, 0)',
      'fill-outline-color': {{
        'base': 1,
        'stops': [
          [0, 'hsla(207, 84%, 57%, 0.24)'],
          [22, 'hsl(207, 84%, 57%)']
        ]
      }},
      'fill-opacity': 1
    }}
  }})

  map.addLayer({{
    'id': 'Highlighted',
    'type': 'fill',
    'source': 'landsat',
    'source-layer': 'Landsat8_Desc_filtr2',
    'paint': {{
      'fill-outline-color': '#1386af',
      'fill-color': '#0f6d8e',
      'fill-opacity': 0.3
    }},
    'filter': ['in', 'PATH', '']
  }})

  map.on('mousemove', (e) => {{
    let features = map.queryRenderedFeatures(e.point, {{layers: ['Grid']}})
    let pr = ['in', 'PATH', '']
    if (features.length !== 0) {{
      pr =  [].concat.apply([], ['any', features.map(e => {{
        return ['all', ['==', 'PATH', e.properties.PATH], ['==', 'ROW', e.properties.ROW]]
      }})])
    }}
    map.setFilter('Highlighted', pr)
  }})

  // From Libra by developmentseed (https://github.com/developmentseed/libra)
  const zeroPad = (n, c) => {{
    let s = String(n)
    if (s.length < c) s = zeroPad('0' + n, c)
    return s
  }}

  map.on('click', (e) => {{
    document.getElementById('loader').classList.toggle('off')
    if (map.getLayer('raster')) map.removeLayer('raster')
    if (map.getSource('raster')) map.removeSource('raster')
    let features = map.queryRenderedFeatures(e.point, {{layers: ['Grid']}})
    if (features.length === 1) {{

      const min_cloud = 0  // add picker
      const max_cloud = 5  // add picker
      const start = moment('2013-01-01').format() // add picker
      const end = moment('2019-08-20').format() // add picker

      const row = zeroPad(features[0].properties.ROW, 3)
      const path = zeroPad(features[0].properties.PATH, 3)

      const body = {{
        "time": `${{start}}/${{end}}`,
        "query": {{
          "eo:column": {{"eq": path}},
          "eo:row": {{"eq": row}},
          "eo:cloud_cover": {{"gte": min_cloud, "lt": max_cloud}},
          "eo:sun_elevation": {{"gt": 0}},
          "landsat:tier": {{"eq": "T1"}},
          "collection": {{"eq": "landsat-8-l1"}},
        }},
        "limit": 1000
    }}

      let url = new URL('{endpoint}/mosaic/create')
      params = {{
        minzoom: 7,
        maxzoom: 12,
        maximum_items_per_tile: 0,
        expr: document.getElementById('ratio-selector').querySelector("input[name='toggle-ratio']:checked").value,
        color_map: 'viridis',
        rescale: '0,0.5',
        pixel_selection: 'stdev',
      }}
      Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

      fetch(url,
        {{
          mode: 'cors',
          method: "POST",
          body: JSON.stringify(body)
        }}
      )
      .then(res => {{
        if (res.ok) return res.json()
        throw new Error('Network response was not ok.')
      }})
      .then(tilejson => {{
        scope.mosaicid = tilejson.name
        map.addSource('raster', {{
          type: 'raster',
          tiles: tilejson.tiles,
          tileSize: 256,
          bounds: tilejson.bounds,
          minzoom: tilejson.minzoom,
          maxzoom: tilejson.maxzoom,
        }})

        map.addLayer({{
          id: 'raster',
          type: 'raster',
          source: 'raster',
        }})
        const bbox = turf.bbox(features[0])
        map.fitBounds([[bbox[0], bbox[1]], [bbox[2], bbox[3]]])
      }})
      .catch(err => {{
        console.warn(err)
      }})
      .then(() => document.getElementById('loader').classList.toggle('off'))

    }} else {{
      console.warn('select only one PR')
    }}
  }})

  document.getElementById('ratio-selector').addEventListener('change', () => {{
    if (map.getLayer('raster')) map.removeLayer('raster')
    if (map.getSource('raster')) map.removeSource('raster')
    if (scope.mosaicid) {{
      let url = new URL(`{endpoint}/tiles/${{scope.mosaicid}}/tilejson.json`)
      params = {{
        expr: document.getElementById('ratio-selector').querySelector("input[name='toggle-ratio']:checked").value,
        color_map: 'viridis',
        rescale: '0,0.5',
        pixel_selection: 'stdev',
      }}
      Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
      map.addSource('raster', {{
        type: 'raster',
        url: url.href,
      }})
      map.addLayer({{
        id: 'raster',
        type: 'raster',
        source: 'raster',
      }})
    }}
  }})
}})
</script>

  </body>
</html>"""
