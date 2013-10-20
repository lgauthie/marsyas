/*
** Copyright (C) 1998-2010 George Tzanetakis <gtzan@cs.uvic.ca>
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU General Public License for more details.
**
** You should have received a copy of the GNU General Public License
** along with this program; if not, write to the Free Software
** Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
*/

#include "SVFilter.h"
#include "../common_source.h"


using namespace Marsyas;


SVFilter::SVFilter(mrs_string name):MarSystem("SVFilter", name)
{
  addControls();
}

SVFilter::~SVFilter()
{
}

MarSystem*
SVFilter::clone() const
{
  return new SVFilter(*this);
}

void
SVFilter::addControls()
{
  addctrl("mrs_real/frequency", 440.0);
  addctrl("mrs_bool/freqin", false);

  setctrlState("mrs_real/frequency", true);
  setctrlState("mrs_bool/freqin", true);
}

void
SVFilter::myUpdate(MarControlPtr sender)
{
  MRSDIAG("SVFilter.cpp - SVFilter:myUpdate");

  freqIn_ = (getctrl("mrs_bool/freqin")->to<mrs_bool>());
  frequency_ = (getctrl("mrs_real/frequency")->to<mrs_real>());
  israte_ = (getctrl("mrs_real/israte")->to<mrs_real>());

  MarSystem::myUpdate(sender);
}

void
SVFilter::myProcess(realvec& in, realvec& out)
{
  mrs_natural t;
	mrs_real fc = frequency_;
	mrs_real fs = 44100.0;

	mrs_real res = 0.5;
	mrs_real drive = 0.02;
	mrs_real freq = 2.0*sin(PI*fmin(0.25, fc/(fs*2)));  // the fs*2 is because it's double sampled
	mrs_real damp = fmin(2.0*(1.0 - pow(res, 0.25)), fmin(2.0, 2.0/freq - freq*0.5));

  for (t = 0; t < inSamples_; t++)
  {
		// the fs*2 is because it's double sampled
		freq = 2.0*sin(PI*fmin(0.25, (freqIn_ ? in(1, t)*israte_: fc)/(israte_*2)));
		damp = fmin(2.0*(1.0 - pow(res, 0.25)), fmin(2.0, 2.0/freq - freq*0.5));

    notch = in(0, t) - damp*band;
    low = low + freq*band;
    high= notch - low;
    band = freq*high + band - drive*band*band*band;
    out(0, t) = 0.5*low;
    notch = in(0, t) - damp*band;
    low = low + freq*band;
    high = notch - low;
    band = freq*high + band - drive*band*band*band;
    out(0, t) += 0.5*low;
  }
}
