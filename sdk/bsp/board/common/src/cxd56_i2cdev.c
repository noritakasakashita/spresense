/****************************************************************************
 * bsp/board/common/src/cxd56_i2cdev.c
 *
 *   Copyright 2018 Sony Semiconductor Solutions Corporation
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 * 3. Neither the name of Sony Semiconductor Solutions Corporation nor
 *    the names of its contributors may be used to endorse or promote
 *    products derived from this software without specific prior written
 *    permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 ****************************************************************************/

/****************************************************************************
 * Included Files
 ****************************************************************************/

#include <sdk/config.h>

#include <stdio.h>
#include <debug.h>
#include <errno.h>

#include "cxd56_i2c.h"

#if defined(CONFIG_CXD56_I2C) && defined(CONFIG_I2C_DRIVER)

/****************************************************************************
 * Name: board_i2cdev_initialize
 *
 * Description:
 *   Initialize and register i2c driver for the specified i2c port
 *
 ****************************************************************************/

int board_i2cdev_initialize(int port)
{
  int ret;
  FAR struct i2c_master_s *i2c;

  _info("Initializing /dev/i2c%d..\n", port);

  /* Initialize i2c deivce */

  i2c = cxd56_i2cbus_initialize(port);
  if (!i2c)
    {
      _err("ERROR: Failed to initialize i2c%d.\n", port);
      return -ENODEV;
    }

  ret = i2c_register(i2c, port);
  if (ret < 0)
    {
      _err("ERROR: Failed to register i2c%d: %d\n", port, ret);
    }

  return ret;
}

/****************************************************************************
 * Name: board_i2cdev_uninitialize
 *
 * Description:
 *   Uninitialize and unregister i2c driver for the specified i2c port
 *
 ****************************************************************************/

#if 0 /* TBD: i2c_unregister() has not been prepared in nuttx. */
int board_i2cdev_uninitialize(int port)
{
  int ret;
  FAR struct i2c_master_s *i2c;

  _info("Finalizing /dev/i2c%d..\n", port);

  /* Finalize i2c deivce */

  ret = i2c_unregister(i2c, port);
  if (ret < 0)
    {
      _err("ERROR: Failed to unregister i2c%d: %d\n", port, ret);
    }

  ret = cxd56_i2cbus_uninitialize(port);
  if (ret)
    {
      _err("ERROR: Failed to finalize i2c%d.\n", port);
      return -ENODEV;
    }

  return ret;
}
#endif

#endif
