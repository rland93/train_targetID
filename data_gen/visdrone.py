import cv2, imagesize, argparse, os, math, tqdm
from pathlib import Path
import numpy

WANTED_ANNOS = {1, 2, 3, 4, 5, 6, 9, 10, 3, 7}
# some categories are a bit too granular (e.g. "bike/tricycle",
# "car/truck/van") so we merge them into a single category.
ANNO_MERGE = {
    1: 15,
    2: 15,
    3: 16,
    4: 16,
    5: 16,
    6: 16,
    9: 16,
    10: 16,
    3: 17,
    7: 17,
}


def process(input_dir, output_dir, verbose):
    odir = Path(output_dir).resolve()
    os.makedirs(odir / "images", exist_ok=True)
    os.makedirs(odir / "labels", exist_ok=True)
    imgspath = Path(input_dir) / "images"
    annotationspath = Path(input_dir) / "annotations"

    imgodir = Path(output_dir) / "images"
    annodir = Path(output_dir) / "labels"
    for i, file in tqdm.tqdm(enumerate(os.listdir(imgspath.resolve()))):
        if i == 25:
            break
        ipath = imgspath.resolve() / file
        apath = annotationspath.resolve() / (ipath.stem + ".txt")
        w, h = imagesize.get(ipath)
        if (w < 640) or (h < 640):
            continue
        # crop factor
        cf = abs(w - h) / 2
        img = cv2.imread(str(ipath))

        # crop w
        if w > h:
            img = img[:, math.ceil(cf) : -math.floor(cf), :]
        # crop h
        elif h > w:
            img = img[math.ceil(cf) : -math.floor(cf), :, :]

        newres = img.shape[0]

        assert img.shape[0] == img.shape[1]

        labrows = []

        # deal with each anno
        with open(apath, "r") as f:
            for ln in f.readlines():
                # split by commas
                anno = [p.strip() for p in ln.split(",")]
                bx = float(anno[0])
                by = float(anno[1])
                bw = float(anno[2])
                bh = float(anno[3])
                if int(anno[5]) in WANTED_ANNOS:
                    cat = ANNO_MERGE[int(anno[5])]
                    # adjust box start/end points
                    if w > h:
                        by -= cf
                    elif h > w:
                        bx -= cf

                    # bbox x0, y0, x1, y1
                    p1, p2, p3, p4 = bx, by, bx + bw, by + bh

                    # clamp bboxes
                    p1, p2 = min(w, max(0, p1)), min(w, max(0, p2))
                    p3, p4 = min(h, max(0, p3)), min(h, max(0, p4))

                    # x case
                    if not ((p1 == w) or (p3 == 0) or (p2 == h) or (p4 == 0)):
                        xcent = str(((p3 - p1) / 2 + p1) / w)
                        ycent = str(((p4 - p2) / 2 + p2) / w)
                        normw = str(bw / w)
                        normh = str(bh / w)

                        row = (str(cat), xcent, ycent, normw, normh)
                        rowj = " ".join(row)
                        labrows.append(rowj)

                else:
                    continue
        with open(str((annodir / ipath.stem).resolve()) + ".txt", "wt") as f:
            f.write("\n".join(labrows))
        # resize image
        img = cv2.resize(img, dsize=(640, 640))

        cv2.imwrite(str(imgodir / ipath.stem) + ".jpg", img)


if __name__ == "__main__":
    argp = argparse.ArgumentParser(
        description="reformat visdrone to compatible yolo fmt"
    )
    argp.add_argument("-i", type=str, required=True, help="input directory")
    argp.add_argument("-o", type=str, required=True, help="output directory")
    argp.add_argument(
        "-d", type=str, required=False, help="dry run. If true, doesn't copy anything."
    )
    opts = argp.parse_args()
    process(opts.i, opts.o, opts.d)
