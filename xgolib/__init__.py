"""
XGO 机器人控制库
统一入口，自动选择设备类型
"""

# 直接导入所有类
from .xgolib_dog import XGO_DOG
from .xgolib_rider import XGO_RIDER

__version__ = '1.4.2'
__all__ = ['XGO', 'XGO_DOG', 'XGO_RIDER']

def XGO(port="/dev/ttyAMA0", baud=115200, version="auto", verbose=False):
    """
    XGO类自动选择对应库的函数
  
    Args:
        port: 串口设备路径
        baud: 波特率
        version: 设备版本 
            "auto" - 自动检测
            "xgomini" - XGO-MINI
            "xgolite" - XGO-LITE  
            "xgomini3w" - XGO-MINI3W
            "xgorider" - XGO-RIDER
        verbose: 是否显示调试信息
    """
    if version == "auto":
        try:
            temp_dog = XGO_DOG(port, baud, version="xgomini", verbose=verbose)
            firmware = temp_dog.read_firmware()
            temp_dog.reset()
            
            print(f"Detected firmware: {firmware}")
            
            if firmware and firmware[0] == 'R':
                print("Auto-detected: XGO-RIDER")
                return XGO_RIDER(port, baud, version="xgorider", verbose=verbose)
            elif firmware and firmware[0] in ['M', 'L', 'W']:
                version_map = {
                    'M': 'xgomini',
                    'L': 'xgolite', 
                    'W': 'xgomini3W'
                }
                detected_version = version_map.get(firmware[0], 'xgomini')
                print(f"Auto-detected: {detected_version.upper()}")
                return XGO_DOG(port, baud, version=detected_version, verbose=verbose)
            else:
                print("Auto-detection failed, using default: XGO-MINI")
                return XGO_DOG(port, baud, version="xgomini", verbose=verbose)
                
        except Exception as e:
            print(f"Auto detection failed: {e}, using default: XGO-MINI")
            return XGO_DOG(port, baud, version="xgomini", verbose=verbose)
    
    elif version in ["xgomini", "xgolite", "xgomini3W"]:
        return XGO_DOG(port, baud, version=version, verbose=verbose)
    
    elif version == "xgorider":
        return XGO_RIDER(port, baud, version=version, verbose=verbose)
    
    else:
        print(f"Warning: Unknown version '{version}', using 'xgomini' instead")
        return XGO_DOG(port, baud, version="xgomini", verbose=verbose)