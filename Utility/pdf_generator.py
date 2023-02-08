from email.mime import image

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, PageTemplate, Image, FrameBreak, PageBreak, Spacer, Paragraph
from reportlab.platypus.frames import Frame
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import pagesizes
from reportlab.platypus.paragraph import Paragraph, ParagraphStyle
from functools import partial
import os
import glob
import pathlib
import sys
import shutil


def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.width + doc.leftMargin + doc.rightMargin - w,
                   doc.height + doc.bottomMargin + doc.topMargin - h)
    canvas.restoreState()


def footer(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.bottomMargin)
    content.drawOn(canvas, doc.leftMargin, h - 130)
    canvas.restoreState()


def row_generation(list_of_images):  # Creates a list of 4 image rows
    for i in range(0, len(list_of_images), 4):
        yield list_of_images[i:i + 4]


def header_and_footer(canvas, doc, header_content, footer_content):
    header(canvas, doc, header_content)
    footer(canvas, doc, footer_content)


def get_image_name_from_path(path: str):
    return pathlib.Path(path).stem

def page_call(page_no):
    print(f"page {page_no} generated")


def generate_pdf(image_dir, filename="generated", progress_func=page_call):

    if 'pdf' not in filename:
        filename = f"{filename}.pdf"

    header_path = pathlib.Path('./assets/logo.png').resolve()
    footer_path = pathlib.Path('./assets/bottom.png').resolve()
    img_dir = pathlib.Path("./").joinpath(image_dir).resolve()
    print(f"path h: {header_path}, f: {footer_path}, img_dir: {img_dir}")

    PAGESIZE = pagesizes.portrait(pagesizes.A4)
    #images = sorted(os.listdir(image_dir))
    images = sorted(img_dir.glob('*.jpg'))
    print(images)

    header_content = Image(header_path, width=350, height=80)#, hAlign='RIGHT')
    footer_content = Image(footer_path, width=500, height=100)#, hAlign='RIGHT')

    styles = getSampleStyleSheet()

    pdf = BaseDocTemplate(filename, pagesize=PAGESIZE,
            leftMargin = 2.2 * cm,
            rightMargin = 2.2 * cm,
            topMargin = 1.5 * cm,
            bottomMargin = 2.5 * cm)

    pdf.setPageCallBack(progress_func)
    main_frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height, id='normal')

    story = []

    fot = partial(header_and_footer, header_content=header_content, footer_content=footer_content)

    spacer1 = Spacer(width=0, height=30)
    spacer2 = Spacer(width=0, height=5)
    paragraph_style = ParagraphStyle(name='caption', alignment=TA_CENTER, fontSize=12)

    frames = []
    frameCount = 2
    frameWidth = (pdf.width) / frameCount
    frameHeight = pdf.height - .05 * cm

    pages_count = len(images)//4
    if len(images) % 4 != 0:
        pages_count += 1
    for page_ind in range(pages_count):
        imgs = [Image(f"{i}", width=180, height=300) for i in list(row_generation(images))[page_ind]]
        print('img ', imgs)

        captions = [
            Paragraph(get_image_name_from_path(i.filename), paragraph_style) for i in imgs
        ]

        if len(imgs) == 1:
            story.extend([
                imgs[0], spacer2, captions[0], PageBreak()
            ])
        elif len(imgs) == 2:
            story.extend([
                imgs[0], spacer2, captions[0], spacer1, FrameBreak(),
                imgs[1], spacer2, captions[1], spacer1, PageBreak()
            ])
        elif len(imgs) == 3:
            story.extend([
                imgs[0], spacer2, captions[0], spacer1, imgs[2], spacer2, captions[2], FrameBreak(),
                imgs[1], spacer2, captions[1], spacer1, PageBreak()
            ])
        elif len(imgs) == 4:
            story.extend([imgs[0], spacer2, captions[0], spacer1, imgs[2], spacer2, captions[2], FrameBreak(),
                          imgs[1], spacer2, captions[1], spacer1, imgs[3], spacer2, captions[3], PageBreak(),
                        ])

        frames.extend([
                Frame(pdf.leftMargin, pdf.topMargin - 10, 200, frameHeight, id=f'normal1_{page_ind}'),
                Frame(pdf.leftMargin + 200 + 150, pdf.topMargin - 10, frameWidth - 200, frameHeight, id=f'normal2_{page_ind}'),
            ])

    pdf.addPageTemplates([
        PageTemplate(id='id1', frames=frames[:2], onPage=fot),
        PageTemplate(id='id2', frames=frames[2:], onPage=fot)
    ])

    print("Generation started\n")
    pdf.build(story)
    print("Generation done\n")
    file_path = pathlib.Path('.').joinpath(filename).resolve()
    print(file_path)

    dest_path = pathlib.Path('./photos/').resolve()
    print("dest path", dest_path)
    if os.path.exists(dest_path.joinpath(file_path.name)):
        os.remove(dest_path.joinpath(file_path.name))
    shutil.move(file_path, dest_path)


