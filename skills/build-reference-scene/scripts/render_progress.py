"""Render real recorded checkpoints; optionally encode PNGs using installed FFmpeg."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess


def executable(value):
    resolved = shutil.which(value) or value
    path = Path(resolved).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError('Executable must be an installed file')
    return str(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', required=True, help='Trusted installed Blender executable')
    parser.add_argument('--ffmpeg', help='Trusted installed FFmpeg; omit for PNG-only delivery')
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--max-edge', type=int, default=720)
    parser.add_argument('--samples', type=int, default=16)
    parser.add_argument('--seconds-per-step', type=float, default=1)
    parser.add_argument('--timeout', type=int, default=1800)
    args = parser.parse_args()
    if not (128 <= args.max_edge <= 1920 and 1 <= args.samples <= 128 and
            .25 <= args.seconds_per_step <= 5 and 1 <= args.timeout <= 3600):
        parser.error('Invalid size, samples, duration or timeout')
    source = args.manifest.resolve(strict=True)
    output = args.output_dir.resolve()
    if output.exists():
        parser.error('Output directory must be new')
    blender = executable(args.blender)
    ffmpeg = executable(args.ffmpeg) if args.ffmpeg else None
    script = Path(__file__).resolve().parents[1] / 'modules/studio/plugins/blender-agent-studio/skills/blender-rendering-workflow/scripts/render_timelapse.py'
    output.mkdir(parents=True, exist_ok=False)
    frames = output / 'frames'
    command = [blender, '--background', '--factory-startup', '--disable-autoexec',
               '--python-exit-code', '1', '--python', str(script), '--',
               '--manifest', str(source), '--output-dir', str(frames),
               '--max-edge', str(args.max_edge), '--samples', str(args.samples)]
    with (output / 'render.log').open('x') as log:
        subprocess.run(command, stdin=subprocess.DEVNULL, stdout=log,
                       stderr=subprocess.STDOUT, check=True, timeout=args.timeout)
    report = json.loads((frames / 'render-manifest.json').read_text())
    if report.get('status') != 'rendered' or not report.get('checkpoints'):
        raise ValueError('Renderer did not produce recorded checkpoints')
    for index in range(len(report['checkpoints'])):
        if not (frames / f'{index:03d}.png').is_file():
            raise ValueError('Missing stage image')
    video = None
    if ffmpeg:
        video = output / 'modeling-timelapse.mp4'
        command = [ffmpeg, '-nostdin', '-n', '-framerate', str(1 / args.seconds_per_step),
                   '-i', str(frames / '%03d.png'), '-c:v', 'libx264', '-r', '24',
                   '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(video)]
        with (output / 'encode.log').open('x') as log:
            subprocess.run(command, stdin=subprocess.DEVNULL, stdout=log,
                           stderr=subprocess.STDOUT, check=True, timeout=args.timeout)
        if not video.is_file() or video.stat().st_size == 0:
            raise ValueError('Encoding produced no video')
    result = {'status': 'encoded' if video else 'frames-rendered',
              'video': str(video) if video else None, 'visual_review': 'pending',
              'frames': str(frames), 'source_manifest': str(source)}
    with (output / 'delivery.json').open('x') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
