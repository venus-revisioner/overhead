from dataclasses import dataclass, field, asdict, astuple
from pathlib import Path
import random

from PIL import Image, ImageChops, ImageStat, ImageOps
import numpy as np

from overhead.toolboxoh import FileManager, ImageCollage


@dataclass
class PythonVenv:
    path: str = Path("D:/PycharmProjects/OpenAI").joinpath("venv3.10", "Scripts", "python.exe").as_posix().__str__()

# --NUMBER-STUFF----------------------------------------------------------------------------
@dataclass
class PrimeNumbers:
    n: int = 10
    prime_list: tuple = ()

    def __post_init__(self):
        self.prime_list = self.amt(self.n)

    def is_prime(self, num):
        if num > 1:
            # check for factors
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                return num

    def amt(self, max_int):
        prime_list = []
        i = 0
        while len(prime_list) < max_int:
            n = self.is_prime(i)
            if n is not None and n > 0:
                prime_list.append(n)
            i += 1
        return tuple(prime_list)

    def up_to(self, max_int):
        prime_list = []
        i = 0
        while i < max_int:
            n = self.is_prime(i)
            if n > 0:
                prime_list.append(n)
            i += 1
        return tuple(prime_list)


@dataclass
class BasicArray:
    base: field(default_factory=(tuple, np.array))

    def __post_init__(self):
        self.base = np.array(self.base)

    @property
    def og(self):
        return self.base

    @property
    def rev(self):
        return self.base[::-1]

    @property
    def ones(self):
        return self.base * 0. + 1.

    @property
    def zeros(self):
        return self.base * 0.




@dataclass
class ArrayOps:
    arr: field(default_factory=(tuple, np.array, list))

    def repeat_me(self, amt=2):
        return np.repeat(self.arr, amt)

    def insert(self, arr_to_insert):
        return np.insert(self.arr, self.arr[1:], arr_to_insert)

    def looper(self, amt=2):
        return self.arr * amt




# --IMAGE-STUFF-----------------------------------------------------------------------------
@dataclass
class BlenderImages:
    best_blenders_file: str = 'blender_images_best_of_best.txt'
    blender_images_path: str = f'D:/Blender/Blender_Generaatiot/'
    best_blenders: FileManager = FileManager(query=best_blenders_file, folder=blender_images_path)
    image_dict: dict = field( init=False, repr=True)

    def __post_init__(self):
        self.image_dict = self.best_blenders.files_full_path

@dataclass
class CNNimages:
    cnn_folder: str = 'Markku_SOURCES'
    cnn_path: str = f'D:\\CNN_images\\{cnn_folder}\\'
    ext_filter = 'resized.jpg'
    sources: FileManager = FileManager(query=cnn_path, ext_filter=ext_filter)
    image_dict: dict = field( init=False, repr=True)

    def __post_init__(self):
        self.image_dict = self.sources.files_full_path


@dataclass
class FindImages:
    path: str
    ext_filter: str = ".jpg"
    image_dict: dict = field( init=False, repr=True)
    verbose: int = 0

    def __post_init__(self):
        self.sources: FileManager = FileManager(query=self.path, ext_filter=self.ext_filter, verbose=self.verbose)
        self.image_dict = self.sources.files_full_path

    def __call__(self, *args, **kwargs):
        return asdict(self)

    @property
    def image_list(self):
        return list(self.image_dict.values())



@dataclass
class CollageFactory:
    img_source: str = ''
    name: str = ''
    resolution: tuple = (4096, 4096)
    shape: tuple = (2, 2)
    img_arr: (list, tuple) = field(default=(), init=False, repr=True)
    img_selection: (list, tuple) = field(default=None, init=False, repr=True)
    img_dest: str = ''
    img_ext_filter: str = ''

    def __post_init__(self):
        if not self.img_dest:
            self.img_dest = self.img_source
        if self.img_dest and Path(self.img_dest).is_dir() is False:
            Path(self.img_dest).mkdir()
        if self.img_arr and self.img_source:
            for e, i in enumerate(self.img_arr):
                self.img_arr[e] = f'{self.img_source}/{i}'
        if not self.img_arr and self.img_source and self.img_ext_filter:
            self.img_arr = FindImages(path=self.img_source, ext_filter=self.img_ext_filter).image_list

    @property
    def dict(self):
        return asdict(self)

    @property
    def tuple(self):
        return astuple(self)

    def make_collage(self, arr=None, name=None, amt=1, randomize=0, mirror=(0,0), flip=(0,0), border=0):
        if arr is None:
            arr = self.img_arr
        if self.img_selection is not None:
            arr = self.img_selection
        for i in range(amt):
            if name is None:
                name = self.name
            if amt > 1:
                name = self.name_index(i)
            if randomize:
                random.shuffle(arr)
            ImageCollage(arr, self.resolution, self.shape, self.img_dest, name=name, mirror=mirror, flip=flip, border=border)

    def name_index(self, idx):
        return f'{Path(self.name).stem}_{idx}{Path(self.name).suffix}'

    def make_many_collages(self, amt=10, randomize=0):
        for i in range(amt):
            if randomize:
                random.shuffle(self.img_arr)
            self.make_collage(self.name_index(i))

    def select_images(self, names):
        arr = []
        for img in self.img_arr:
            for name in names:
                if name in img:
                    arr.append(img)
                    print("MATCH", img)
        self.img_selection = arr
        print("\nImage selection:", self.img_selection)


@dataclass
class ImgAnalysis:
    img: (Image.Image, str)
    extrema: (list, tuple)= ()
    count: str = ""
    sum: str = ""
    sum2: str = ""
    mean: str = ""
    median: str = ""
    rms: str = ""
    var: str = ""
    stddev: str = ""

    def __post_init__(self):
        if isinstance(self.img, str):
            self.img = Image.open(self.img)
        self.extrema = [ImageStat.Stat(self.img).h[i] for i in range(3)]
        self.count = ImageStat.Stat(self.img).h[0]
        print("EXTREMA: ",self.extrema)
        print("COUNT:", self.count)




@dataclass
class ImgChops:
    img1_path: (None,str) = None
    img2_path: (None,str) = None
    enhance_type: str = ""
    img1: Image.Image = None
    img2: Image.Image = None
    _img_out: Image.Image = None

    def __post_init__(self):
        if isinstance(self.img1_path, str):
            self.img1 = Image.open(self.img1_path)
        else:
            self.img1 = self.img1_path
        if isinstance(self.img2_path, str):
            self.img2 = Image.open(self.img2_path)
        else:
            self.img2 = self.img2_path

    @property
    def out(self):
        if self._img_out is None:
            return eval(f'ImageChops.{self.enhance_type}(self.img1, self.img2)')
        else:
            return self._img_out


    def post_process(self, enhance_type, **kwargs):
        self._img_out = eval(f'ImageChops.{enhance_type}(self._img_out, **kwargs)')

    def evaluate(self, enhance_type, image, **kwargs):
        return eval(f'ImageChops.{enhance_type}(image1=self.{image}, image2=self._img_out, **kwargs)')

    def evaluate_single(self, img, func_str, **kwargs):
        self._img_out = eval(func_str)

    def self_process(self, enhance_type, image='img1', **kwargs):
        self._img_out = eval(f'ImageChopz§zs.{enhance_type}(self.{image}, **kwargs)')

    def two(self, enhance_type, image1='img1', image2='img2', **kwargs):
        if self.img1.size == self.img2.size:
            self._img_out = eval(f'ImageChops.{enhance_type}(image1=self.{image1}, image2=self.{image2}, **kwargs)')
        else:
            print(f'Cannot perform {enhance_type}: size mismatch!')
            print(f'{image1}: {self.img1.size} -- {image2}: {self.img2.size}')
    def add(self, enhance_type, img='img1', **kwargs):
        self.enhance_type = enhance_type
        if self._img_out is None:
            self._img_out = self.out
        self._img_out = self.evaluate(self.enhance_type ,img, **kwargs)

    def chain(self, enhance_list):
        self.enhance_type = enhance_list[0]
        for item in enhance_list[1:]:
            self.add(enhance_type=item)

    def overwrite(self, img_path='img1'):
        if Path(img_path).is_file() is False:
            # print(img_path, "IS NO FILE, generating...")
            img_path = f'self.{img_path}_path'
        eval(f'self._img_out.save({img_path})')

    def offset(self, img=None, xoffset=0, yoffset=None):
        out_path = ""
        if img is None:
            if self.img1 is not None:
                img = self.img1
                out_path = self.img1_path
        if isinstance(img, str):
            if Path(img).is_file() is False:
                # print(img, "IS NO IMAGE, generating...")
                img = f'self.{img})'
                out_path = f'self.{img}_path)'
        if yoffset is None:
            yoffset = xoffset
        self._img_out = ImageChops.offset(img, xoffset, yoffset)
        self._img_out.save(out_path)

    def crop(self, border):
        self._img_out = ImageOps.expand(self.img1, border=border, fill=(127,127,127))
        self._img_out.save(self.img1_path)
